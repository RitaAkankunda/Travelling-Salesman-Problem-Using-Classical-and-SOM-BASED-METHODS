def tsp_dfs(graph, start):
    """
    Uses DFS backtracking to solve the TSP.
    Returns the complete cycle (including return to start) and its total distance.
    """
    best_path = None
    best_distance = float('inf')
    
    def dfs(path, visited, current_distance):
        nonlocal best_path, best_distance
        current = path[-1]
        # Base case: all nodes have been visited.
        if len(visited) == len(graph):
            # Check for an edge from current back to start to complete the cycle.
            for neighbor, d in graph[current]:
                if neighbor == start:
                    total = current_distance + d
                    # If a complete tour is found that is better than any previous, update.
                    if total < best_distance:
                        best_distance = total
                        best_path = path + [start]
            return
        
        # Explore unvisited neighbors, sorted by edge distance (lowest first).
        for neighbor, d in sorted(graph[current], key=lambda x: x[1]):
            if neighbor not in visited:
                dfs(path + [neighbor], visited | {neighbor}, current_distance + d)
    
    dfs([start], {start}, 0)
    return best_path, best_distance

# Graph representation
graph = {
    1: [(2, 12), (3, 10), (7, 12)],
    2: [(1, 12), (3, 8), (4, 12)],
    3: [(1, 10), (2, 8), (4, 11), (5, 3), (7, 9)],
    4: [(2, 12), (3, 11), (5, 11), (6, 10)],
    5: [(3, 3), (4, 11), (6, 6), (7, 7)],
    6: [(4, 10), (5, 6), (7, 9)],
    7: [(1, 12), (3, 9), (5, 7), (6, 9)]
}

# Run the DFS TSP algorithm starting at node 1
complete_path, total_distance = tsp_dfs(graph, 1)

# Format the route as specified.
# (The complete_path includes the return to the start. We omit that for printing the "route".)
if complete_path:
    route = " > ".join(map(str, complete_path))
    print("Route:", route)
    print("Total Distance:", total_distance)
else:
    print("No complete tour found.")
