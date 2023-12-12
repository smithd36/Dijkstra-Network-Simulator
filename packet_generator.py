# packet_generator.py
# Authors: Ghaith Ishaq, Drey Smith

import numpy as np

def generate_packets(nodes_count, lambda_param=0.5):
    """
    Generate packets at sources with a Poission distribution

    :param nodes_count: The number of nodes (sources) to generate packets for.
    :param lambda_param: Lambda parameter for exponential distribution.
                        Default is set to 0.5 for a moderate packet generation rate.

    :return: A list of all generated packets, each represented as a python dictionary.
            Each packet dictionary has attributes: 'source' (node index), 'arrival_time',
            and 'size' (size of packet).
    """
    packets = []

    for node in range(nodes_count):
        # generate an inter-arrival time with exponential distribution
        inter_arrival_time = np.random.exponential(scale=1/lambda_param)

        # random packet size with uniform distribution betweem 0 and
        packet_size = np.random.uniform(0, 1)
        
        # dictionary representative of a generated packet
        packet = {'source': node, 'arrival_time': inter_arrival_time, 'size': packet_size}

        # add to list of all packets
        packets.append(packet)

    return packets