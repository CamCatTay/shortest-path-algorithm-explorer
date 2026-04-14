import random

def generate_random_graph(num_nodes, num_edges, min_weight=1, max_weight=10, seed=None, directed=False):
    """Generate a random weighted graph as an adjacency dict.

    num_nodes  -- total number of nodes (labeled 0 to num_nodes-1)
    num_edges  -- number of edges to add
    min_weight -- minimum edge weight (inclusive)
    max_weight -- maximum edge weight (inclusive)
    seed       -- optional seed for reproducibility
    directed   -- if True, edges are one-way; if False, edges are bidirectional

    returns adjacency dict: {node: [(neighbor, weight), ...]}
    """
    if seed is not None:
        random.seed(seed)

    # initialize empty adjacency list for every node
    graph = {i: [] for i in range(num_nodes)}

    existing_edges = set()

    # Build a spanning path through a random permutation of all nodes so that
    # every node is reachable from node 0 regardless of edge direction.
    perm = list(range(num_nodes))
    random.shuffle(perm)
    # Ensure node 0 is the start so the default source is always connected.
    perm.remove(0)
    perm = [0] + perm

    # For directed graphs, build a lookup of each node's position in the
    # permutation so that extra edges can be restricted to forward-only
    # (perm_pos[u] < perm_pos[v]).  This makes the graph a DAG (No cycles), which
    # guarantees no negative-weight cycles even when weights are negative.
    perm_pos = {node: i for i, node in enumerate(perm)} if directed else {}

    edges_added = 0
    for i in range(num_nodes - 1):
        u, v = perm[i], perm[i + 1]
        weight = random.randint(min_weight, max_weight)
        graph[u].append((v, weight))
        existing_edges.add((u, v))
        if not directed:
            graph[v].append((u, weight))
            existing_edges.add((v, u))
        edges_added += 1
        if edges_added >= num_edges:
            break

    # Fill remaining edge budget with random edges
    attempts = 0
    max_attempts = num_edges * 10
    while edges_added < num_edges and attempts < max_attempts:
        attempts += 1
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)

        if u == v or (u, v) in existing_edges:
            continue

        # For directed graphs, only allow forward edges in permutation order
        # to keep the graph cycle-free (DAG), preventing negative-weight cycles.
        if directed and perm_pos[u] >= perm_pos[v]:
            continue

        weight = random.randint(min_weight, max_weight)
        graph[u].append((v, weight))
        existing_edges.add((u, v))
        if not directed:
            graph[v].append((u, weight))
            existing_edges.add((v, u))
        edges_added += 1

    return graph
