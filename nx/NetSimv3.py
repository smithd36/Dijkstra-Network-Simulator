import networkx as nx
import numpy as np
import time
import random

def read_from_file(filename):
    # read the network in from network.txt
    with open(filename, 'r') as file:
        lines = file.readlines()
        nodes_count, edges_count = map(int, lines[0].split())
        # skips delimiter
        edges = [tuple(map(int, line.split())) for line in lines[1:] if not line.startswith('**')]

    G = nx.Graph()
    G.add_nodes_from(range(nodes_count))
    G.add_edges_from(edges)

    return G

def generate_network(nodes_count):
    # randomly generate a connected graph
    while True:
        G = nx.erdos_renyi_graph(nodes_count, p=0.2)
        if nx.is_connected(G):
            break

    # assign bandwidth and delay to the links
    for (u, v) in G.edges():
        G[u][v]['bandwidth'] = np.random.uniform(0, 1)
        G[u][v]['delay'] = np.random.uniform(1, 10)

    # Initialize 'bandwidth' for all edges
    for (u, v) in G.edges():
        if 'bandwidth' not in G[u][v]:
            G[u][v]['bandwidth'] = 0

    return G

def write_to_file(graph, filename):
    # write the network information to a file
    with open(filename, 'w') as file:
        file.write(f"{graph.number_of_nodes()} {graph.number_of_edges()}\n")
        for (u, v) in graph.edges():
            file.write(f"{u} {v}\n")

def generate_packets(node_count, lambda_param=0.5):
    # generate packets at sources with Poisson distribution
    packets = []
    for node in range(node_count):
        inter_arrival_time = np.random.exponential(scale=1/lambda_param)
        packets.append({'source': node, 'arrival_time': inter_arrival_time, 'size': np.random.uniform(0, 1)})

    return packets

class Router:
    def __init__(self, graph, max_queue_size=30, service_rate=1.0):
        self.graph = graph
        self.input_queue = []
        self.output_queue = []
        self.max_queue_size = max_queue_size
        self.service_rate = service_rate

    def enqueue_packet(self, packet):
        # queueing logic
        if len(self.input_queue) < self.max_queue_size:
            self.input_queue.append(packet)

    def service_packets(self, current_time):
        for packet_info in self.input_queue:
            packet = packet_info['packet']
            path = packet_info['path']

            # Calculate transmission time based on bandwidth
            transmission_time = packet['size'] / self.output_bandwidth(path)

            # Add propagation delay
            propagation_delay = self.output_delay(path)

            # Update arrival time and transmission time
            packet['arrival_time'] = current_time
            packet['transmission_time'] = transmission_time + propagation_delay

            # Assuming the packet is successfully transmitted to the next router
            self.output_queue.append(packet)

        # Clear the input queue after servicing
        self.input_queue = []

    def output_bandwidth(self, path):
        # Calculate available bandwidth on the output link of the router
        # For simplicity, this function assumes uniform bandwidth across all links
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            # Set a default bandwidth value if 'bandwidth' key is missing
            bandwidth = self.graph[edge[0]][edge[1]].get('bandwidth', 1.0)
            
            # Check if bandwidth is zero to avoid division by zero
            if bandwidth == 0:
                print(f"Warning: Bandwidth is zero for edge {edge}")
                print(f"Graph: {self.graph}")
                return 0  # Return 0 as a default value
    
        return min(self.graph[path[i]][path[i + 1]].get('bandwidth', 1.0) for i in range(len(path) - 1))



    def output_delay(self, path):
        # Calculate total propagation delay along the output link of the router
        return sum(self.graph[path[i]][path[i+1]]['delay'] for i in range(len(path)-1))

class Simulation:
    def __init__(self, graph, routers, packets):
        self.graph = graph
        self.routers = routers
        self.packets = packets
        self.total_generated_packets = 0
        self.successfully_transmitted_packets = 0
        self.total_transmission_time = 0
        self.max_completion_time = 0
        self.min_completion_time = float('inf')
        self.total_dropped_packets = 0
        self.max_dropped_packets = 0
        self.min_dropped_packets = float('inf')

    def simulate(self, simulation_time=1000):
        start_time = time.time()
        current_time = 0

        while current_time < simulation_time:
            # generate packets based on the Poisson distribution
            new_packets = generate_packets(len(self.graph.nodes()))
            self.packets.extend(new_packets)
            self.total_generated_packets += len(new_packets)

            # send packets through the network
            for packet in self.packets:
                source = packet['source']
                destination = random.choice([node for node in self.graph.nodes() if node != source])
                path = nx.shortest_path(self.graph, source=source, target=destination)
                self.routers[source].enqueue_packet({'path': path, 'packet': packet})

            # service the packets at a router
            for router in self.routers.values():
                router.service_packets(current_time)

            # update the network state
            current_time = time.time() - start_time

        # for statistics
        for router in self.routers.values():
            # update completion time
            if router.output_queue:
                completion_time = router.output_queue[-1]['packet']['arrival_time'] + router.output_queue[-1]['transmission_time']
                self.max_completion_time = max(self.max_completion_time, completion_time)
                self.min_completion_time = min(self.min_completion_time, completion_time)

            # update the dropped packets if any
            dropped_packets = len(router.input_queue)
            self.total_dropped_packets += dropped_packets
            self.max_dropped_packets = max(self.max_dropped_packets, dropped_packets)
            self.min_dropped_packets = min(self.min_dropped_packets, dropped_packets)

        # percentage of successfully received packets
        self.successfully_transmitted_packets = self.total_generated_packets - self.total_dropped_packets
        success_percentage = (self.successfully_transmitted_packets / self.total_generated_packets) * 100

        # average packet transmission time
        if self.successfully_transmitted_packets > 0:
            self.total_transmission_time /= self.successfully_transmitted_packets

        # Print statistics
        print("Simulation Results:")
        print(f"Total number of packets generated: {self.total_generated_packets}")
        print(f"Total number of packets successfully transmitted: {self.successfully_transmitted_packets}")
        print(f"Percentage of successfully received packets: {success_percentage:.2f}%")
        print(f"Average packet transmission time: {self.total_transmission_time:.2f} seconds")
        print(f"Maximum completion time for transmissions: {self.max_completion_time:.2f} seconds")
        print(f"Minimum completion time for transmissions: {self.min_completion_time:.2f} seconds")
        print(f"Maximum number of packets dropped at a router: {self.max_dropped_packets}")
        print(f"Minimum number of packets dropped at a router: {self.min_dropped_packets}")
        print(f"Average number of packets dropped at a router: {self.total_dropped_packets / len(self.routers):.2f}")

if __name__ == "__main__":
    # set the seed value for reproducibility
    seed = 42
    filename = "network.txt"

    # read in a graph or generate a connected network
    if filename:
        graph = read_from_file(filename)
    else:
        nodes_count = 150
        graph = generate_network(nodes_count)
        write_to_file(graph, "generated_graph.txt")

    # make routers and packets
    routers = {node: Router(graph) for node in graph.nodes()}
    packets = generate_packets(len(graph.nodes()))

    # create a new simulation
    simulation = Simulation(graph, routers, packets)

    # run
    simulation.simulate(simulation_time=10)
