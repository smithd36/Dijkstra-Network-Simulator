# network_generator.py
# Authors: Drey Smith, Ghaith Ishaq

import networkx as nx
import numpy as np

def generate_network(nodes_count, seed):
    """Randomly generate a connected graph with bandwidth and delay assigned to links."""
    # set a seed for reproducability
    np.random.seed(seed)
    
    while True:
        G = nx.erdos_renyi_graph(nodes_count, p=0.2)
        if nx.is_connected(G):
            break

    # Assign bandwidth and delay to the links
    for (u, v) in G.edges():
        G[u][v]['bandwidth'] = np.random.uniform(0, 1)
        G[u][v]['delay'] = np.random.uniform(1, 10)

    # Initialize 'bandwidth' for all edges
    for (u, v) in G.edges():
        if 'bandwidth' not in G[u][v]:
            G[u][v]['bandwidth'] = 0

    return G