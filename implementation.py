# Imports

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

# Output Writer

# Main Function