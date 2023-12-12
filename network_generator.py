# network_generator.py
# Authors: Drey Smith, Ghaith Ishaq

import networkx as nx
import numpy as np

def generate_network(nodes_count, seed):
<<<<<<< HEAD
    """
    Randomly generates a connected graph with bandwidth and delay assigned to links.

    :param nodes_count: The number of nodes in the generated network.
    :param seed: Seed for reproducibility of the random graph generation.

    :return: A connected graph (networkx.Graph) with randomly assigned bandwidth and delay to links.
    """
=======
    """Randomly generate a connected graph with bandwidth and delay assigned to links."""
>>>>>>> 71ec412572f873ebd92a6226713b4acc7c8f72a6
    # set a seed for reproducability
    np.random.seed(seed)
    
    while True:
        G = nx.erdos_renyi_graph(nodes_count, p=0.2)
        if nx.is_connected(G):
            break

    # assign bandwidth and delay to the links
    for (u, v) in G.edges():
        G[u][v]['bandwidth'] = np.random.uniform(0, 1)
        G[u][v]['delay'] = np.random.uniform(1, 10)

    # initalize 'bandwidth' for all edges
    for (u, v) in G.edges():
        if 'bandwidth' not in G[u][v]:
            G[u][v]['bandwidth'] = 0

    return G