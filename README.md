# Network Simulation

A Python implementation of a discrete event network simulator, developed for the semester project of the course CS 440: Computer Networks. The simulator models the functioning of a computer network, including node connectivity, link properties, packet generation, queuing, and routing.

This repository contains a network simulation program that simulates the transmission of packets through a network of routers. The simulation is designed to model various aspects of network communication, including bandwidth, delay, and packet transmission.

## Table of Contents
- [Project Structure](#project-structure)
  - [Classes and Methods](#classes-and-methods)
    - [1. `file_handler.py`](#1-file_handlerpy)
    - [2. `network_generator.py`](#2-network_generatorpy)
    - [3. `packet_generator.py`](#3-packet_generatorpy)
    - [4. `router.py`](#4-routerpy)
    - [5. `simulation.py`](#5-simulationpy)
- [Dependencies and How to Run](#dependencies-and-how-to-run)
- [Simulation Duration](#simulation-duration)
- [Simulation Results](#simulation-results)
- [Team Members/Contributors](#team-memberscontributors)

# Project Structure
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

#### `display_results()`
- **Description:** Displays the results of the simulation in a Tkinter window.
- **Parameters:** `self` (object): The instance of the `NetworkSimulation` class.

## Dependencies and How to Run

### 1. Prerequisites
Before installing and running the network simulator, make sure you are running Python 3.11.3.

### 2. Dependencies
Extract the contents of the zip file to a directory of your choice. Then, navigate to the directory in a terminal and run the following command to install the required dependencies:
- `pip install -r requirements.txt`

### 3. Run
There are 2 ways to use the network simulator:

### 1. Network Generation
Run the following command to generate a network graph and check for connectivity:
`python3 main.py <seed>`
- `<seed>`: The seed value for random number generation.

### 2. Network Simulation
Run the following command to simulate the network that exists in a <b>.txt</b> file:
- `python3 main.py <seed> <graph_filename.txt>`

## Simulation Duration

You can adjust the duration of the network simulation by modifying the `simulation_time` parameter in the `main.py` file. Follow these steps to change the simulation time:

1. Open the `main.py` file in a text editor of your choice.

2. Locate the following section of the code:

    ```python
    # main.py
    # Authors: Ghaith Ishaq, Drey Smith

    # ... (other imports and code)

    # create a new simulation
    simulation = NetworkSimulation(graph, routers, packets)

    # run the simulation
    (LINE 40):simulation.simulate(simulation_time=1000)
    ```

3. Update the `simulation_time` parameter in line 40 with the desired duration in seconds. For example, to simulate the network for 20 seconds, change the line to:

    ```python
    simulation.simulate(simulation_time=20)
    ```

4. Save the changes to the `main.py` file.

Now, when you run the simulation using `python3 main.py <seed> [<graph_filename.txt>]` or `python3 main.py <seed>`, it will use the specified simulation time. Adjusting this parameter allows you to control the duration of the network simulation.

## Simulation Results

After running the simulation, these statistics will be displayed in a Tkinter Window:
- Total Packets Generated
- Successfully Transmitted Packets
- Success Percentage
- Average Transmission Time
- Max Completion time
- Min Completion Time
- Max Dropped Packets
- Min Dropped Packets
- Avg Dropped Packets

<img src="https://github.com/smithd36/DiscreteEvent-NetSim/assets/90289165/e6ba53ee-e0d1-46bd-8e45-0ddb551b77a3"/>

### 3. Team Members/Contributors
- Drey Smith
- Ghaith Ishaq