# main.py
# Authors: Ghaith Ishaq, Drey Smith

from file_handler import read_from_file, write_to_file
from network_generator import generate_network
from packet_generator import generate_packets
from router import Router
from simulation import NetworkSimulation

def main():
    # Set the seed value for reproducibility
    seed = 42
    filename = "network.txt"

    # Read in a graph or generate a connected network
    if filename:
        graph = read_from_file(filename)
    else:
        nodes_count = 150
        graph = generate_network(nodes_count)
        write_to_file(graph, "generated_graph.txt")

    # Make routers and packets
    routers = {node: Router(graph) for node in graph.nodes()}
    packets = generate_packets(len(graph.nodes()))

    # Create a new simulation
    simulation = NetworkSimulation(graph, routers, packets)

    # Run the simulation
    simulation.simulate(simulation_time=10)

if __name__ == "__main__":
    main()