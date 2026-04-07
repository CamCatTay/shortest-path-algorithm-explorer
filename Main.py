from Graph_Generation import generate_random_graph
from Dijkstras import dijkstras_algorithm, print_analytics


def main():
    # generate a small reproducible graph for demonstration
    graph = generate_random_graph(num_nodes=6, num_edges=10, seed=42)

    print("graph adjacency list:")
    for node, edges in sorted(graph.items()):
        print(f"  {node}: {edges}")
    print()

    source = 0
    target = 5

    # run with a specific target
    print(f"shortest path from {source} to {target}:")

    path = dijkstras_algorithm(graph, source=source, target=target)

    print(" -> ".join(str(n) for n in path) if path else "no path found")
    print()
    print("analytics (single target run):")
    print_analytics()
    print()

    # run for all destinations from source
    print(f"all shortest paths from node {source}:")

    dijkstras_algorithm(graph, source=source)

    print_analytics()


if __name__ == "__main__":
    main()
