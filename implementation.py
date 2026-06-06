"""
Assignment 1 - PS13 - Communication Networks
Implementation of Dijkstra's Algorithm and Ant Colony Optimization (ACO)
"""

# Imports
import heapq
import random

# ==========================================
# Graph & Utility Functions
# ==========================================
def read_graph(filename: str):
    """
    Parses the input file to generate the graph, source, and destination nodes.
    Expects the file to start with the number of nodes and edges, followed by
    the edge definitions, and ending with the source and destination nodes.
    
    Args:
        filename (str): The path to the input text file.
        
    Returns:
        tuple: (graph dictionary, source node, destination node)
    """
    graph = {}
    try:
        with open(filename,"r") as file:
            n = int(file.readline().strip())
            m = int(file.readline().strip())

            for i in range(n):
                graph[i] = []

            for _ in range(m):
                line = file.readline().strip()
                if not line:
                    continue
                u,v,w = map(int,line.split())

                if u<0 or u>=n:
                    raise ValueError(f"Invalie node {u}")
                
                if v<0 or v>=n:
                    raise ValueError(f"Invalid node {v}")
                
                if w<=0:
                    raise ValueError("Latency must be positive")
                

                graph[u].append((v,w))
                graph[v].append((u,w))

            source = int(file.readline().strip())
            dest = int(file.readline().strip())

            if source not in graph or dest not in graph:
                raise ValueError("Invalid source or destination node")
            
            return graph,source,dest
    except FileNotFoundError:
        print("Input file not found")

# Input Parser

# ==========================================
# Deterministic Algorithm: Dijkstra
# ==========================================
def reconstruct_path(parent, source, destination):
    """
    Backtracks from the destination node to the source using the parent dictionary
    to reconstruct the shortest path taken by Dijkstra's algorithm.
    """

    path = []

    current = destination

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    if path[0] != source:
        return None

    return path

def dijkstra(graph,source,destination):
    """
    Finds the absolute minimum latency path using Dijkstra's deterministic algorithm.
    
    Args:
        graph (dict): The adjacency list representing the network.
        source (int): Starting router.
        destination (int): Target router.
        
    Returns:
        tuple: (Shortest path as a list, Minimum latency cost)
    """
    dist = {
        node: float('inf')
        for node in graph
    }
    parent = {
        node: None
        for node in graph
    }
    dist[source] = 0

    pq = [(0,source)]
    while pq:
        current_dist,current_node = heapq.heappop(pq)
        if current_dist>dist[current_node]:
            continue
        if current_node == destination:
            break
        for neighbor,weight in graph[current_node]:
            new_dist = current_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = current_node

                heapq.heappush(pq,
                               (new_dist,neighbor))
    
    if dist[destination] == float('inf'):
        return None,None
    path = reconstruct_path(parent,source,destination)
    return path,dist[destination]

def format_path(path):
    """
    Formats the path list into a readable string format.
    
    Args:
        path (list): List of nodes representing the path.
        
    Returns:
        str: Formatted string (e.g., "0 -> 1 -> 2")
    """
    if path is None:
        return "No Valid Path Found"
    return " -> ".join(
        map(str, path)
    )
graph, source, destination = read_graph("inputPS13.txt")

print(graph)
print("Source:", source)
print("Destination:", destination)
path, cost = dijkstra(graph,source,destination)
print("Path:",format_path(path))
print("Cost:",cost)

# ==========================================
# Meta-Heuristic Algorithm: Ant Colony Optimization
# ==========================================
def initialize_pheromones(graph):
    """
    Initializes the pheromone levels (tau) on all edges to a baseline value of 1.0.
    """
    pheromone = {}
    for node in graph:
        for neighbor,weight in graph[node]:
            pheromone[(node,neighbor)] = 1.0
        
    return pheromone

pheromone = initialize_pheromones(graph)
print(f"Pheromones: {pheromone}")

#Initialize Heuristic between nodes
def initialize_heuristic(graph):
    """
    Calculates the heuristic desirability (eta) for all edges.
    Defined as the inverse of the edge latency.
    """
    heuristic = {}

    for node in graph:
        for neighbor,weight in graph[node]:
            heuristic[(node,neighbor)] = 1.0/weight
        
    return heuristic

heuristic = initialize_heuristic(graph)

for edge, value in heuristic.items():
    print(edge, round(value, 3))


def choose_next_node(current_node,candidates,pheromone,heuristic,alpha,beta):
    """
    Probabilistically selects the next node for an ant to move to, 
    based on the pheromone trail and heuristic desirability.
    """
    if not candidates:
        return None
    
    desirabilities = []

    for candidate in candidates:
        tau = pheromone[(current_node,candidate)]
        eta = heuristic[(current_node,candidate)]
        value = (tau**alpha)*(eta**beta)
        desirabilities.append(value)
    total = sum(desirabilities)
    
    if total==0:
        return random.choice(candidates)
    probabilities = [
        value/total for value in desirabilities
    ]

    next_node = random.choices(candidates,weights=probabilities,k=1)[0]
    return next_node

for _ in range(10):

    print(
        choose_next_node(
            0,
            [1, 2, 4],
            pheromone,
            heuristic,
            alpha=1.0,
            beta=2.0
        )
    )

def construct_ant_path(graph,source,destination,pheromone,heuristic,alpha,beta):
    """
    Simulates a single ant traversing the network from source to destination.
    """
    current_node = source
    path = [source]
    visited = set()
    visited.add(source)
    steps = 0
    max_steps = len(graph)
    while current_node!=destination:
        candidates = []
        steps+=1
        
        # Prevent infinite loops in cyclic graphs
        if steps>max_steps:
            return None
            
        # Identify valid, unvisited neighbors
        for neighbor,weight in graph[current_node]:
            if neighbor not in visited:
                candidates.append(neighbor)

        # Dead end reached
        if not candidates:
            return None
        
        next_node = choose_next_node(current_node,candidates,pheromone,heuristic,alpha,beta)

        path.append(next_node)
        visited.add(next_node)
        current_node = next_node
    return path

# Test Run
for i in range(10):

    path = construct_ant_path(
        graph,
        source,
        destination,
        pheromone,
        heuristic,
        alpha=1.0,
        beta=2.0
    )

    print(path)

def calculate_cost(path,graph):
    """
    Calculates the total latency of a given path.
    """
    if path is None:
        return float('inf')
    total_cost = 0
    for i in range(len(path)-1):
        current_node = path[i]
        next_node = path[i+1]

        edge_found = False

        for neighbor,weight in graph[current_node]:
            if neighbor == next_node:
                total_cost+=weight
                edge_found = True
                break
        if not edge_found:
            raise ValueError(f"Edge ({current_node},{next_node}) not found in graph")
        
    return total_cost

path = [0,1,2,4]
cost = calculate_cost(path,graph)
print(f"Cost : {cost}")

def evaporate_pheromones(pheromone,rho):
    """
    Applies the evaporation rate to all existing pheromones in the network.
    Formula: tau = tau * (1 - rho)
    """
    for edge in pheromone:
        pheromone[edge]*=(1-rho)

def deposit_pheromones(pheromone,ant_solutions,Q):
    """
    Deposits new pheromones on the trails utilized by the ants in the current iteration.
    Ants with shorter paths (lower latency cost) deposit more pheromone.
    """
    for path,cost in ant_solutions:
        if path is None:
            continue

        if cost ==0:
            continue

        delta_tau = Q/cost

        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            # Since graph is undirected, update both directions
            pheromone[(u,v)]+=delta_tau
            
            pheromone[(v,u)]+=delta_tau

# ACO Function
def ant_colony_optimization(graph,source,destination,num_ants,alpha,beta,rho,iterations,Q):
    """
    Orchestrates the overall Ant Colony Optimization meta-heuristic process.
    
    Returns:
        tuple: (best_path, best_cost, convergence_iteration)
    """
    pheromone = initialize_pheromones(graph)
    heuristic = initialize_heuristic(graph)

    best_path = None
    best_cost = float('inf')
    
    convergence_iteration = 0

    for iteration in range(iterations):
        ant_solutions = []
        iteration_best_cost = float('inf')

        # Send out the fleet of ants
        for _ in range(num_ants):
            path = construct_ant_path(graph,source,destination,pheromone,heuristic,alpha,beta)
            if path is None:
                continue
            cost = calculate_cost(path,graph)

            ant_solutions.append((path,cost))

            if cost < iteration_best_cost:
                iteration_best_cost = cost

            # Global best tracker
            if cost < best_cost:
                best_cost = cost
                best_path = path
                # Record when the new optimal path is discovered
                convergence_iteration = iteration+1

        # Environment update step
        evaporate_pheromones(pheromone,rho)

        deposit_pheromones(pheromone,ant_solutions,Q)

    return (best_path,best_cost,convergence_iteration)

best_path_1,best_cost_1,conv_1 = (ant_colony_optimization(
    graph,
    source,
    destination,
    num_ants=10,
    alpha=1.0,
    beta=2.0,
    rho=0.5,
    iterations=100,
    Q=100
))

print(f"Scenario 1: Path: {format_path(best_path_1)}")
print(f"Cost : {best_cost_1}")
print(f"Convergence: {conv_1}")


best_path_2,best_cost_2,conv_2 = (ant_colony_optimization(
    graph,
    source,
    destination,
    num_ants=10,
    alpha=2.5,
    beta=1.0,
    rho=0.3,
    iterations=100,
    Q=100
))

print(f"Scenario 2: Path: {format_path(best_path_2)}")
print(f"Cost : {best_cost_2}")
print(f"Convergence: {conv_2}")

dijkstra_path, dijkstra_cost = dijkstra(
    graph,
    source,
    destination
)
print("\nDijkstra")
print("Path:", format_path(dijkstra_path))
print("Cost:", dijkstra_cost)


# ==========================================
# Output Generation
# ==========================================
def write_output(filename,scenario1,scenario2,dijkstra_result):
    with open(filename,"w") as file:
        path1, cost1, conv1 = scenario1
        path2, cost2, conv2 = scenario2
        d_path,d_cost = dijkstra_result

        file.write("Scenario 1\n")
        file.write(f"Best Path: {format_path(path1)}\n")
        file.write(f"Minimum Latency: {cost1}\n")
        file.write(f"Covergence Iteration: {conv1}\n\n")
        
        file.write("Scenario 2\n")
        file.write(f"Best Path: {format_path(path2)}\n")
        file.write(f"Minimum Latency: {cost2}\n")
        file.write(f"Covergence Iteration: {conv2}\n\n")
        
        file.write("DIJKSTRA \n")
        file.write(f"Best Path: {format_path(d_path)}\n")
        file.write(f"Minimum Latency: {d_cost}\n\n")
        
        file.write("Comparison\n")
        if conv1<conv2:
            file.write("Scenario 1 converged faster than scenario 2\n")
        elif conv2 <conv1:
            file.write("Scenario 2 converged faster than Scenario 1\n")
        else:
            file.write("Both scenario converged at the same iteration\n")

        file.write(f"Dijkstra Optimal Cost: {d_cost}\n")


# ==========================================
# Main Execution Block
# ==========================================
graph,source,destination = read_graph("inputPS13.txt")

dijkstra_path,dijkstra_cost = dijkstra(graph,source,destination)

scenario1 = ant_colony_optimization(graph,
                                    source,
                                    destination,
                                    num_ants=10,
                                    alpha=1.0,
                                    beta=2.0,
                                    rho=0.5,
                                    iterations=100,
                                    Q=100)

scenario2 = ant_colony_optimization(graph,
                                    source,
                                    destination,
                                    num_ants=10,
                                    alpha=2.5,
                                    beta=1.0,
                                    rho=0.3,
                                    iterations=100,
                                    Q=100)

write_output(
    "outputPS13.txt",
    scenario1,
    scenario2,
    (dijkstra_path,dijkstra_cost)
)

print("\nDijkstra")
print(format_path(dijkstra_path))
print(dijkstra_cost)

print("\nScenario 1")
print(format_path(scenario1[0]))
print(scenario1[1])

print("\nScenario 2")
print(format_path(scenario2[0]))
print(scenario2[1])
