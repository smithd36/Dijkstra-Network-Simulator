# packet_generator.py
# Authors: Ghaith Ishaq, Drey Smith

import numpy as np

def generate_packets(nodes_count, lambda_param=0.5):
    """Generate packets at sources with Poission distribution"""
    packets = []
    for node in range(nodes_count):
        inter_arrival_time = np.random.exponential(scale=1/lambda_param)
        packets.append({'source': node, 'arrival_time': inter_arrival_time, 'size': np.random.uniform(0, 1)})

    return packets