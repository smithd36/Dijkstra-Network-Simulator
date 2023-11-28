import networkx as nx
import numpy as np
import time

def generate_network(nodes_count):
    # the first step is to randomly generat a graph with nodes and ranom edges
    G = nx.erdos_renyi_graph(nodes_count, p=0.2)
    
    # verify a connection
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(nodes_count, p=0.2)
    
    # assign bandwitch and delay to the links
    for (u, v) in G.edges():
        G[u][v]['bandwidth'] = np.random.uniform(0, 1)
        G[u][v]['delay'] = np.random.uniform(1 , 10)

    return G

def write_to_file(graph, filename):
    # write the nodes and edges to a file
    with open(filename, 'w') as file:
        file.write(f"{graph.number_of_nodes()} {graph.number_of_edges()}\n")
        for (u, v) in graph.edges():
            file.write(f"{u} {v}\n")

def generate_packets(node_count, lambda_param=0.5):
    # generate the packets at sources with Poission distribution
    packets = []
    for node in range(node_count):
        inter_arrival_time = np.random.exponential(scale=1/lambda_param)
        packets.append({'source': node, 'arrival_time': inter_arrival_time, 'size': np.random.uniform(0, 1)})

    return packets


def create_routing_table(graph):
    # dijkstra's algo for routing table creation for each router
    routing_tables = {}
    for node in graph.nodes():
        shortest_paths = nx.single_source_dijkstra_path_length(graph, node)
        routing_tables[node] = shortest_paths

    return routing_tables


def main():
    nodes_count = 150
    graph = generate_network(nodes_count)
    packets = generate_packets(nodes_count)
    routers = {node: Router() for node in graph.nodes()}
    routing_tables = create_routing_table(graph)

    # simulation instance
    simulation = Simulation(graph, routers, packets)

    # run
    simulation.simulate(simulation_time=10)


class Router:
    def __init__(self, max_queue_size=30, service_rate=1.0):
        self.input_queue = []
        self.output_queue = []
        self.max_queue_size = max_queue_size
        self.service_rate = service_rate

    def enqueue_packet(self, packet):
        # queueing logic
        pass

    def service_packets(self):
        # service packets from input using exponential distribution
        pass

class Simulation:
    def __init__(self, graph, routers, packets):
        self.graph = graph
        self.routers = routers
        self.packets = packets


    def simulate(self, simulation_time=10):
        start_time = time.time()
        current_time = 0

        while current_time < simulation_time:

            # generate packets based upon the Poisson distribution
            new_packets = generate_packets(len(self.graph.nodes()))
            self.packets.extend(new_packets)

            # send packets through the network
            for packet in self.packets:
                source = packet['source']
                destination = np.random.choice([node for node in self.graph.nodes() if node != source])
                path = nx.shortest_path(self.graph, source=source, target=destination)
                self.routers[source].enqueue_packet({'path': path, 'packet': packet})

            # service the packets at a router
            for router in self.routers.values():
                router.service_packets()

            # update the network state
            current_time = time.time() - start_time


if __name__ == "__main__":
    main()