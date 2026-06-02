# Imports
import heapq

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
# Output Writer

# Main Function