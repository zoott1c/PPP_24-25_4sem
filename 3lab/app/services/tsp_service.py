from app.schemas.tsp import Graph, PathResult

def calculate_shortest_path(graph: Graph) -> PathResult:
    nodes = graph.nodes
    edges = graph.edges

    neighbors = {node: [] for node in nodes}
    for u, v in edges:
        neighbors[u].append(v)
        neighbors[v].append(u)

    current = nodes[0]
    path = [current]
    visited = {current}

    while len(visited) < len(nodes):
        found = False
        for neighbor in neighbors[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                current = neighbor
                found = True
                break
        if not found:
            break

    total_distance = float(len(path))

    return PathResult(path=path, total_distance=total_distance)
