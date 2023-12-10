# simulation.py
# Authors: Ghaith Ishaq, Drey Smith

import time
import random
from router import Router
from packet_generator import generate_packets
import networkx as nx

class NetworkSimulation:
    """Class represents the simulation of the network with a graph, routers and packets."""
    def __init__(self, graph, routers, packets):
        """Initialize the simulation with a graph, routers, and packets."""
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
        """Run the simulation for a specified duration."""
        start_time = time.time()
        current_time = 0

        while current_time < simulation_time:
            # Generate packets based on the Poisson distribution
            new_packets = generate_packets(len(self.graph.nodes()))
            self.packets.extend(new_packets)
            self.total_generated_packets += len(new_packets)

            # Send packets through the network
            for packet in self.packets:
                source = packet['source']
                destination = random.choice([node for node in self.graph.nodes() if node != source])
                path = nx.shortest_path(self.graph, source=source, target=destination)
                self.routers[source].enqueue_packet({'path': path, 'packet': packet})

            # Service the packets at each router
            for router in self.routers.values():
                router.service_packets(current_time)

            # Update the network state
            current_time = time.time() - start_time

        # Calculate statistics
        for router in self.routers.values():
            # Update completion time
            if router.output_queue:
                completion_time = router.output_queue[-1]['packet']['arrival_time'] + router.output_queue[-1]['transmission_time']
                self.max_completion_time = max(self.max_completion_time, completion_time)
                self.min_completion_time = min(self.min_completion_time, completion_time)

            # Update dropped packets count
            dropped_packets = len(router.input_queue)
            self.total_dropped_packets += dropped_packets
            self.max_dropped_packets = max(self.max_dropped_packets, dropped_packets)
            self.min_dropped_packets = min(self.min_dropped_packets, dropped_packets)

        # Calculate the percentage of successfully received packets
        self.successfully_transmitted_packets = self.total_generated_packets - self.total_dropped_packets
        success_percentage = (self.successfully_transmitted_packets / self.total_generated_packets) * 100

        # Calculate average packet transmission time
        if self.successfully_transmitted_packets > 0:
            self.total_transmission_time /= self.successfully_transmitted_packets

        # Print simulation results
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