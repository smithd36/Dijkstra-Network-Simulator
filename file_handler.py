"""
Utility file to manage reading from a file and writing to a file.

Authors: Ghaith Ishaq, Drey Smith
"""
import networkx as nx

def read_from_file(filename):
    """Read network information from a file and return a NetworkX graph."""
    # read the network in from network.txt
    with open(filename, 'r') as file:
        lines = file.readlines()
        nodes_count, edges_count = map(int, lines[0].split())
        
        # skips delimiter with line.startswith(**)
        edges = [tuple(map(int, line.split())) for line in lines[1:] if not line.startswith('**')]

    G = nx.Graph()
    G.add_nodes_from(range(nodes_count))
    G.add_edges_from(edges)

    return G


def write_to_file(graph, filename):
    """Write network information to a file."""
    with open(filename, 'w') as file:
        file.write(f"{graph.number_of_nodes()} {graph.number_of_edges()}\n")
        for (u, v) in graph.edges():
            file.write(f"{u} {v}\n")