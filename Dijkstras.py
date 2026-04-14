import heapq
import time

# global variables
_runtime_seconds = 0.0
_all_paths = {}  # maps each reachable node to its full path from source
_all_costs = {}  # maps each reachable node to its total path cost


def dijkstras_algorithm(graph, source, target=None):
    global _runtime_seconds, _all_paths, _all_costs

    # track predecessor of each node to reconstruct paths
    prev = {node: None for node in graph}

    # get start time prior to running algorithm for analysis
    start_time = time.perf_counter()

    # --- start dijkstra's ---

    # initialize distances to infinity for all nodes except source
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    pq = [(0, source)] # (distance to node)

    visited = set()

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        # nodes that were already visited are skipped
        if current_node in visited:
            continue
        else:
            visited.add(current_node)

        # early exit when only the path to target is needed (NOT required)
        if target is not None and current_node == target:
            break

        # edge relaxation
        for neighbor, weight in graph.get(current_node, []):
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev[neighbor] = current_node # (NOT required)
                heapq.heappush(pq, (new_dist, neighbor))

        #return distances

    # --- end dijkstra's ---

    _runtime_seconds = time.perf_counter() - start_time

    # reconstruct path for a single node
    def _reconstruct(node):
        path = []
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
        # return empty list if node was unreachable
        return path if path[0] == source else []

    if target is not None:
        path = _reconstruct(target)
        _all_paths = {target: path}
        _all_costs = {target: distances[target]}
        return path

    # build paths for every reachable node
    _all_paths = {}
    _all_costs = {}
    for node in graph:
        if distances[node] < float('inf'):
            _all_paths[node] = _reconstruct(node)
            _all_costs[node] = distances[node]

    return _all_paths


def print_dijkstras_analytics():
    print(f"paths found: {len(_all_paths)}")
    for destination, path in sorted(_all_paths.items(), key=lambda x: str(x[0])):
        path_str = ' → '.join(str(n) for n in path) if path else 'unreachable'
        cost = _all_costs.get(destination)
        cost_str = f" (Cost: {cost})" if cost is not None else ''
        print(f"  {cost_str} Target: {destination}: {path_str}")

    print(f"\nruntime: {_runtime_seconds:.6f} seconds")
