# simulation.py
# Authors: Ghaith Ishaq, Drey Smith

import time
import random
from router import Router
from packet_generator import generate_packets
import networkx as nx
import tkinter as tk
from tkinter import scrolledtext

class NetworkSimulation:
    """Class represents the simulation of the network with a graph, routers and packets."""
    def __init__(self, graph, routers, packets):
        """
        Initialize the simulation with a graph, routers, and packets.

        :param graph: The network graph representing connectivity between routers.
        :param routers: Dictionary of routers in the network.
        :param packets: List of packets to be simulated in the network.
        """        
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

        # other attributes for simulation stats
        self.success_percentage = 0
        self.avg_dropped_packets = 0

        # set state for Tkinter window
        self.results_window = None
        self.results_text = None

    def display_results(self):
        """Display simulation results in a Tkinter window."""
        if self.results_window is None:
            self.results_window = tk.Tk()
            self.results_window.title("Simulation Results")

            # adjust width and height as needed
            self.results_text = scrolledtext.ScrolledText(self.results_window, wrap=tk.WORD, width=70, height=30)
            self.results_text.pack()

        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, "Simulation Results:\n")
        self.results_text.insert(tk.END, f"Total number of packets generated: {self.total_generated_packets}\n")
        self.results_text.insert(tk.END, f"Total number of packets successfully transmitted: {self.successfully_transmitted_packets}\n")
        self.results_text.insert(tk.END, f"Percentage of successfully received packets: {self.success_percentage:.2f}%\n")
        self.results_text.insert(tk.END, f"Average packet transmission time: {self.total_transmission_time:.2f} seconds\n")
        self.results_text.insert(tk.END, f"Maximum completion time for transmissions: {self.max_completion_time:.2f} seconds\n")
        self.results_text.insert(tk.END, f"Minimum completion time for transmissions: {self.min_completion_time:.2f} seconds\n")
        self.results_text.insert(tk.END, f"Maximum number of packets dropped at a router: {self.max_dropped_packets}\n")
        self.results_text.insert(tk.END, f"Minimum number of packets dropped at a router: {self.min_dropped_packets}\n")
        self.results_text.insert(tk.END, f"Average number of packets dropped at a router: {self.avg_dropped_packets:.2f}\n")

        self.results_window.mainloop()

    def simulate(self, simulation_time=1000):
        """
        Run the simulation for a specified duration.

        :param simulation_time: The duration of the simulation in seconds.
        """ 
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

            # service the packets at each router
            for router in self.routers.values():
                router.service_packets(current_time)

            # update the network state
            current_time = time.time() - start_time

        # calculate the required statistics
        for router in self.routers.values():
            # update completion time
            if router.output_queue:
                completion_time = router.output_queue[-1]['packet']['arrival_time'] + router.output_queue[-1]['transmission_time']
                self.max_completion_time = max(self.max_completion_time, completion_time)
                self.min_completion_time = min(self.min_completion_time, completion_time)

            # update dropped packets count
            dropped_packets = len(router.input_queue)
            self.total_dropped_packets += dropped_packets
            self.max_dropped_packets = max(self.max_dropped_packets, dropped_packets)
            self.min_dropped_packets = min(self.min_dropped_packets, dropped_packets)

        # calculate the percentage of successfully received packets
        self.successfully_transmitted_packets = self.total_generated_packets - self.total_dropped_packets
        success_percentage = (self.successfully_transmitted_packets / self.total_generated_packets) * 100

        # calculate average packet transmission time
        if self.successfully_transmitted_packets > 0:
            self.total_transmission_time /= self.successfully_transmitted_packets

<<<<<<< HEAD
        # show results in window
        self.display_results()
=======
        # print simulation results
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
>>>>>>> 71ec412572f873ebd92a6226713b4acc7c8f72a6
