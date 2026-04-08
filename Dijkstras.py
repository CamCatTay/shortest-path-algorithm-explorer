import heapq
import time

# global state populated by dijkstras_algorithm
_runtime_seconds = 0.0
_all_paths = {}  # maps each reachable node to its full path from source
_all_costs = {}  # maps each reachable node to its total path cost


def dijkstras_algorithm(graph, source, target=None):
    """Run Dijkstra's shortest-path algorithm.

    graph  -- adjacency dict: {node: [(neighbor, weight), ...]}
    source -- starting node
    target -- optional destination node; if None, compute paths to all vertices

    returns the shortest path (list of nodes) to target, or a dict of all
    shortest paths keyed by destination node when target is None.
    """
    global _runtime_seconds, _all_paths, _all_costs

    # initialize distances to infinity for all nodes except source
    dist = {node: float('inf') for node in graph}
    dist[source] = 0

    # track predecessor of each node to reconstruct paths
    prev = {node: None for node in graph}

    # min-heap entries are (distance, node)
    heap = [(0, source)]

    visited = set()

    start_time = time.perf_counter()

    while heap:
        current_dist, current_node = heapq.heappop(heap)

        if current_node in visited:
            continue
        visited.add(current_node)

        # early exit when only the path to target is needed
        if target is not None and current_node == target:
            break

        for neighbor, weight in graph.get(current_node, []):
            new_dist = current_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current_node
                heapq.heappush(heap, (new_dist, neighbor))

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
        _all_costs = {target: dist[target]}
        return path

    # build paths for every reachable node
    _all_paths = {}
    _all_costs = {}
    for node in graph:
        if dist[node] < float('inf'):
            _all_paths[node] = _reconstruct(node)
            _all_costs[node] = dist[node]

    return _all_paths


def print_dijkstras_analytics():
    """Print runtime and all paths recorded by the last algorithm run."""
    print(f"runtime: {_runtime_seconds:.6f} seconds")
    print(f"paths found: {len(_all_paths)}")
    for destination, path in sorted(_all_paths.items(), key=lambda x: str(x[0])):
        path_str = ' → '.join(str(n) for n in path) if path else 'unreachable'
        cost = _all_costs.get(destination)
        cost_str = f" (Cost: {cost})" if cost is not None else ''
        print(f"  {cost_str} Target: {destination}: {path_str}")
