# main.py
# Authors: Ghaith Ishaq, Drey Smith

import sys
from file_handler import read_from_file, write_to_file
from network_generator import generate_network
from packet_generator import generate_packets
from router import Router
from simulation import NetworkSimulation

def main():
    # check command-line args
    if len(sys.argv) == 3:
        seed = int(sys.argv[1])
        filename = sys.argv[2]
    elif len(sys.argv) == 2:
        seed = int(sys.argv[1])
        filename = None
    else:
<<<<<<< HEAD
        # improper invocation from command line
=======
        # impropor invocation from command line
>>>>>>> 71ec412572f873ebd92a6226713b4acc7c8f72a6
        print("Usage:\npython3 main.py <seed> [<graph_filename.txt>]\nOR\npython3 main.py <seed>")
        sys.exit(1)

    # read in a graph or generate a connected network
    if filename:
        graph = read_from_file(filename)
    else:
        nodes_count = 150
        graph = generate_network(nodes_count, seed)
        write_to_file(graph, "generated_graph.txt")

    # make routers and packets
    routers = {node: Router(graph) for node in graph.nodes()}
    packets = generate_packets(len(graph.nodes()), seed)

    # create a new simulation
    simulation = NetworkSimulation(graph, routers, packets)

    # run the simulation
<<<<<<< HEAD
    simulation.simulate(simulation_time=1000)
=======
    simulation.simulate(simulation_time=10)
>>>>>>> 71ec412572f873ebd92a6226713b4acc7c8f72a6

if __name__ == "__main__":
    main()