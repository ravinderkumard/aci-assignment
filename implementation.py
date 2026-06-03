# Imports
import heapq
import random

# Graph Functions
def read_graph(filename: str):
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

# Dijkstra Algorithm
def reconstruct_path(parent, source, destination):

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

#Initialize Pheromones for path between current node and neighbor node.
def initialize_pheromones(graph):
    pheromone = {}
    for node in graph:
        for neighbor,weight in graph[node]:
            pheromone[(node,neighbor)] = 1.0
        
    return pheromone

pheromone = initialize_pheromones(graph)
print(f"Pheromones: {pheromone}")

#Initialize Heuristic between nodes
def initialize_heuristic(graph):
    heuristic = {}

    for node in graph:
        for neighbor,weight in graph[node]:
            heuristic[(node,neighbor)] = 1.0/weight
        
    return heuristic

heuristic = initialize_heuristic(graph)

for edge, value in heuristic.items():
    print(edge, round(value, 3))


# How ant chooses the next route.
def choose_next_node(current_node,candidates,pheromone,heuristic,alpha,beta):
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

# Single ant to travel from the source router to the destination router.
def construct_ant_path(graph,source,destination,pheromone,heuristic,alpha,beta):
    current_node = source
    path = [source]
    visited = set()
    visited.add(source)
    steps = 0
    max_steps = len(graph)
    while current_node!=destination:
        candidates = []
        steps+=1
        if steps>max_steps:
            return None
        
        for neighbor,weight in graph[current_node]:
            if neighbor not in visited:
                candidates.append(neighbor)

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
# Output Writer

# Main Function