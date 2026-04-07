from Graph_Generation import generate_random_graph
from Dijkstras import dijkstras_algorithm, print_analytics


def main():
    # generate a small reproducible graph for demonstration

    # dense graph
    #graph = generate_random_graph(num_nodes=6, num_edges=12, seed=42)

    # sparse graph
    graph = generate_random_graph(num_nodes=6, num_edges=6, seed=42)

    # negative weight graph
    #graph = generate_random_graph(num_nodes=6, num_edges=6, seed=42, min_weight=-10)

    # large sparse graph (time trial)
    #graph = generate_random_graph(num_nodes=500, num_edges=600, seed=42)

    # large dense graph (time trial)
    #graph = generate_random_graph(num_nodes=500, num_edges=5000, seed=42)

    # large negative weight graph (time trial - bellman-ford only)
    #graph = generate_random_graph(num_nodes=500, num_edges=600, seed=42, min_weight=-10)


    print("graph adjacency list:")
    for node, edges in sorted(graph.items()):
        print(f"  {node}: {edges}")
    print()

    # write edge list to file to reproduce visually on https://csacademy.com/app/graph_editor/.
    with open("graph_data.txt", "w") as f:
        for node, edges in sorted(graph.items()):
            for neighbor, weight in edges:
                f.write(f"{node} {neighbor} {weight}\n")
    print("graph data written to graph_data.txt")
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
