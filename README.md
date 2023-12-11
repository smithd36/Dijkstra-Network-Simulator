# Network Simulation

This repository contains a network simulation program that simulates the transmission of packets through a network of routers. The simulation is designed to model various aspects of network communication, including bandwidth, delay, and packet transmission.

## Classes and Methods

### 1. `file_handler.py`

#### `read_from_file(filename)`

- **Description:** Reads network information from a file.
- **Parameters:**
  - `filename` (str): The name of the file containing the network information.
- **Returns:**
  - `G` (NetworkX graph): The network graph.

#### `write_to_file(graph, filename)`

- **Description:** Writes network information to a file.
- **Parameters:**
  - `graph` (NetworkX graph): The network graph to be written to the file.
  - `filename` (str): The name of the file to write the network information to.

### 2. `network_generator.py`

#### `generate_network(nodes_count, seed)`

- **Description:** Generates a random connected network graph with specified properties.
- **Parameters:**
  - `nodes_count` (int): The number of nodes in the network.
  - `seed` (int): The seed value for random number generation.
- **Returns:**
  - `G` (NetworkX graph): The generated network graph.

### 3. `packet_generator.py`

#### `generate_packets(node_count, seed=None)`

- **Description:** Generates packets at sources with a Poisson distribution.
- **Parameters:**
  - `node_count` (int): The number of nodes in the network.
  - `seed` (int, optional): The seed value for random number generation. Default is `None`.
- **Returns:**
  - `packets` (list of dicts): List of generated packets.

### 4. `router.py`

#### `Router(graph, max_queue_size=30, service_rate=1.0)`

- **Description:** Represents a router in the network.
- **Parameters:**
  - `graph` (NetworkX graph): The network graph.
  - `max_queue_size` (int): Maximum size of the router's input queue. Default is `30`.
  - `service_rate` (float): Rate at which the router processes packets. Default is `1.0`.

#### `enqueue_packet(packet)`

- **Description:** Adds a packet to the router's input queue.
- **Parameters:**
  - `packet` (dict): Information about the packet.

#### `service_packets(current_time)`

- **Description:** Services packets in the input queue, updating transmission times.

#### `output_bandwidth(path)`

- **Description:** Calculates available bandwidth on the output link of the router.
- **Parameters:**
  - `path` (list): Path of the packet through the network.

#### `output_delay(path)`

- **Description:** Calculates total propagation delay along the output link of the router.
- **Parameters:**
  - `path` (list): Path of the packet through the network.

### 5. `simulation.py`

#### `NetworkSimulation(graph, routers, packets)`

- **Description:** Represents a network simulation.
- **Parameters:**
  - `graph` (NetworkX graph): The network graph.
  - `routers` (dict): Dictionary of routers in the network.
  - `packets` (list): List of generated packets.

#### `simulate(simulation_time=1000)`

- **Description:** Runs the network simulation.
- **Parameters:**
  - `simulation_time` (int): The duration of the simulation in seconds. Default is `1000`.