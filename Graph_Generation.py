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

    edges_added = 0
    attempts = 0
    max_attempts = num_edges * 10

    while edges_added < num_edges and attempts < max_attempts:
        attempts += 1
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)

        # skip self-loops and duplicate edges
        if u == v:
            continue
        if any(neighbor == v for neighbor, _ in graph[u]):
            continue

        weight = random.randint(min_weight, max_weight)
        graph[u].append((v, weight))

        # add reverse edge when undirected
        if not directed:
            graph[v].append((u, weight))
        edges_added += 1

    return graph
