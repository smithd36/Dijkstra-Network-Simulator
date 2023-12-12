# router.py
# Authors: Ghaith Ishaq, Drey Smith
import networkx as nx
import numpy as np

class Router:
    """Class representing the router with a graph, max queue size and service rate."""
    def __init__(self, graph, max_queue_size=30, service_rate=1.0):
        """
        Initialize a router with a graph, maximum queue size, and service rate.

        :param graph: The network graph representing connectivity between routers.
        :param max_queue_size: Maximum size of the input queue for the router.
        :param service_rate: The rate at which the router can process packets.
        """
        self.graph = graph
        self.input_queue = []
        self.output_queue = []
        self.max_queue_size = max_queue_size
        self.service_rate = service_rate

    def enqueue_packet(self, packet):
        """
        Queue a packet in the input queue if space is available.

        :param packet: The packet to be enqueued, represented as a dictionary.
        """
        if len(self.input_queue) < self.max_queue_size:
            self.input_queue.append(packet)

    def service_packets(self, current_time):
        """
        Service packets in the input queue, updating transmission times.

        :param current_time: The current time in the simulation.
        """        
        for packet_info in self.input_queue:
            packet = packet_info['packet']
            path = packet_info['path']

            # calculate transmission time based on bandwidth
            transmission_time = packet['size'] / self.output_bandwidth(path)

            # add propagation delay
            propagation_delay = self.output_delay(path)

            # update arrival time and transmission time
            packet['arrival_time'] = current_time
            packet['transmission_time'] = transmission_time + propagation_delay

            # assuming the packet is successfully transmitted to the next router
            self.output_queue.append({'packet': packet, 'transmission_time': transmission_time})

        # empty input queue after servicing
        self.input_queue = []

    def output_bandwidth(self, path):
        """
        Calculate available bandwidth on the output link of the router.

        :param path: The path of the packet through the network.
        :return: The available bandwidth on the output link.
        """        
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            bandwidth = self.graph[edge[0]][edge[1]].get('bandwidth', 1.0)
            
            # check if bandwidth is zero to avoid division by zero
            if bandwidth == 0:
                return 0  # return 0 as a default value
    
        return min(self.graph[path[i]][path[i + 1]].get('bandwidth', 1.0) for i in range(len(path) - 1))

    def output_delay(self, path):
        """
        Calculate total propagation delay along the output link of the router.

        :param path: The path of the packet through the network.
        :return: The total propagation delay along the output link.
        """        
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            delay = self.graph[edge[0]][edge[1]].get('delay', 0)
            
            # check if delay is zero to avoid potential issues
            if delay == 0:
                return 0  # return 0 as a default value

        return sum(self.graph[path[i]][path[i + 1]].get('delay', 0) for i in range(len(path) - 1))