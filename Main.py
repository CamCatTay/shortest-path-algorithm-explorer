import os

from Graph_Generation import generate_random_graph
from Dijkstras import dijkstras_algorithm, print_dijkstras_analytics
from BellmanFord import bellman_ford_algorithm, print_bellman_ford_analytics

W = 56  # box width
APP_TITLE = 'SHORTEST PATH ALGORITHM EXPLORER'

# box drawing helpers

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def row(text=''):
    inner = W - 4
    print('║  ' + str(text)[:inner].ljust(inner) + '║')

def sep():
    print('╠' + '═' * (W - 2) + '╣')

def top():
    print('╔' + '═' * (W - 2) + '╗')

def bot():
    print('╚' + '═' * (W - 2) + '╝')

def header(subtitle):
    top()
    print('║' + APP_TITLE.center(W - 2) + '║')
    sep()
    print('║' + subtitle.center(W - 2) + '║')
    bot()
    print()

# preset graph definitions (Sparse = V * 2; Dense = V * V)

PRESETS = [
    {'name': 'Small Dense',               'num_nodes': 6,   'num_edges': 12,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': False},
    {'name': 'Small Sparse',              'num_nodes': 6,   'num_edges': 6,    'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': False},
    {'name': 'Small Negative Weight',     'num_nodes': 6,   'num_edges': 6,    'seed': 42, 'min_weight': -10, 'max_weight': 10, 'directed': True},
    {'name': 'Large Sparse','num_nodes': 500, 'num_edges': 600,  'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': False},
    {'name': 'Large Dense','num_nodes': 500, 'num_edges': 5000, 'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': False},
    {'name': 'Large Negative Weight','num_nodes': 500, 'num_edges': 600,  'seed': 42, 'min_weight': -10, 'max_weight': 10, 'directed': True},

    {'name': 'Time Trial 1 (Sparse)',               'num_nodes': 10,   'num_edges': 10*2,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
    {'name': 'Time Trial 2 (Sparse)',               'num_nodes': 100,   'num_edges': 100*2,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
    {'name': 'Time Trial 3 (Sparse)',               'num_nodes': 5000,   'num_edges': 5000*2,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
    {'name': 'Time Trial 4 (Sparse)',               'num_nodes': 10000,   'num_edges': 10000*2,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
    {'name': 'Time Trial 5 (Sparse)',               'num_nodes': 20000,   'num_edges': 20000*2,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},

    {'name': 'Time Trial 1 (Dense)',               'num_nodes': 10,   'num_edges': 10*10,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
    {'name': 'Time Trial 2 (Dense)',               'num_nodes': 50,   'num_edges': 50*50,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
    {'name': 'Time Trial 3 (Dense)',               'num_nodes': 250,   'num_edges': 250*250,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
    {'name': 'Time Trial 4 (Dense)',               'num_nodes': 500,   'num_edges': 500*500,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
    {'name': 'Time Trial 5 (Dense)',               'num_nodes': 1000,   'num_edges': 1000*1000,   'seed': 42, 'min_weight': 1,   'max_weight': 10, 'directed': True},
]

# graph helpers

def build_graph(params):
    return generate_random_graph(
        num_nodes=params['num_nodes'],
        num_edges=params['num_edges'],
        seed=params.get('seed'),
        min_weight=params.get('min_weight', 1),
        max_weight=params.get('max_weight', 10),
        directed=params.get('directed', False),
    )

def activate(entry):
    """Build the graph dict on first use and update graph_data.txt."""
    if entry['graph'] is None:
        print('  Generating graph...')
        entry['graph'] = build_graph(entry['params'])
    with open('graph_data.txt', 'w') as f:
        for node, edges in sorted(entry['graph'].items()):
            for neighbor, weight in edges:
                f.write(f'{node} {neighbor} {weight}\n')
    return entry

# screens

def print_main_menu(current, source, target):
    clear()
    t_str = str(target) if target is not None else 'none  (all nodes)'
    g_str = current['name'] if current else 'none selected'

    top()
    print('║' + APP_TITLE.center(W - 2) + '║')
    sep()
    row(f'Graph  :  {g_str}')
    row(f'Source :  {source}    Target :  {t_str}')
    sep()
    row('1.  Choose a graph')
    row('2.  Create a graph')
    row('3.  Set source node')
    row('4.  Set target node')
    row('5.  Display current selections')
    row("6.  Run Dijkstra's algorithm")
    row("7.  Run Bellman-Ford algorithm")
    row('8.  Clear screen')
    row('9.  Exit')
    bot()
    print()


def screen_choose(graphs):
    clear()
    header(' CHOOSE A GRAPH ')
    for i, g in enumerate(graphs, 1):
        p = g['params']
        w_range = f"[{p.get('min_weight', 1)}, {p.get('max_weight', 10)}]"
        seed_str = str(p.get('seed', 'rand'))
        print(f"  {i:>2}.  {g['name']}")
        print(f"        nodes={p['num_nodes']}  edges={p['num_edges']}  "
              f"weights={w_range}  seed={seed_str}")
        print()
    print('   0.  Back')
    print()
    choice = input('  Select: ').strip()
    if not choice or choice == '0':
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(graphs):
            return activate(graphs[idx])
        print('\n  Invalid selection.')
    except ValueError:
        print('\n  Invalid input.')
    input('  Press Enter to continue...')
    return None


def screen_create(graphs):
    clear()
    header(' CREATE A GRAPH ')
    print('  Leave a field blank to use the default.')
    print()

    def get_int(p_text, default):
        v = input(f'  {p_text} [{default}]: ').strip()
        return int(v) if v else default

    try:
        num_nodes  = get_int('Number of nodes', 6)
        num_edges  = get_int('Number of edges', 6)
        min_weight = get_int('Min weight',      1)
        max_weight = get_int('Max weight',      10)
        seed_in    = input(  '  Seed           (blank = random): ').strip()
        seed       = int(seed_in) if seed_in else None
        dir_in     = input(  '  Directed?      (y/n) [n]: ').strip().lower()
        directed   = dir_in == 'y'
        name       = input(  '  Graph name: ').strip() or 'Custom Graph'
    except ValueError:
        print('\n  Invalid input — graph not created.')
        input('  Press Enter to continue...')
        return graphs, None

    params = {
        'name': name,
        'num_nodes': num_nodes, 'num_edges': num_edges,
        'min_weight': min_weight, 'max_weight': max_weight,
        'seed': seed, 'directed': directed,
    }
    entry = {'name': name, 'params': params, 'graph': None}
    activate(entry)
    graphs.append(entry)
    print(f"\n  Graph '{name}' created.")
    input('  Press Enter to continue...')
    return graphs, entry


def screen_selections(current, source, target):
    clear()
    header(' CURRENT SELECTIONS ')
    if not current:
        print('  No graph selected.')
    else:
        p = current['params']
        print(f"  Graph    : {current['name']}")
        print(f"  Nodes    : {p['num_nodes']}")
        print(f"  Edges    : {p['num_edges']}")
        print(f"  Weights  : [{p.get('min_weight', 1)}, {p.get('max_weight', 10)}]")
        print(f"  Seed     : {p.get('seed', 'random')}")
        print(f"  Directed : {p.get('directed', False)}")
        if p['num_nodes'] <= 20:
            print()
            print('  Adjacency list:')
            for node, edges in sorted(current['graph'].items()):
                print(f'    {node}: {edges}')
    print()
    print(f"  Source   : {source}")
    print(f"  Target   : {target if target is not None else 'none (all nodes)'}")
    print()
    input('  Press Enter to continue...')


def screen_set_node(current, kind, current_val):
    clear()
    is_target = kind == 'target'
    subtitle = ' SET TARGET NODE ' if is_target else ' SET SOURCE NODE '
    header(subtitle)

    if current:
        n = current['params']['num_nodes']
        print(f'  Current graph : {current["name"]}')
        print(f'  Valid range   : 0  to  {n - 1}')
    else:
        print('  No graph selected — node will be validated when a graph is chosen.')
    print()

    blank_hint = 'blank = none (all nodes)' if is_target else 'blank = 0'
    val = input(f'  Enter node  ({blank_hint}): ').strip()

    if val == '':
        return None if is_target else 0

    try:
        node = int(val)
    except ValueError:
        print(f'\n  "{val}" is not a valid integer.')
        input('  Press Enter to continue...')
        return current_val

    if current and node not in current['graph']:
        n = current['params']['num_nodes']
        print(f'\n  Node {node} is out of range. Valid nodes are 0 to {n - 1}.')
        input('  Press Enter to continue...')
        return current_val

    return node


def screen_run_dijkstras(current, source, target):
    clear()
    header(" RUN DIJKSTRA'S ALGORITHM ")
    if not current:
        print('  No graph selected. Choose or create a graph first.')
        input('  Press Enter to continue...')
        return

    graph = current['graph']
    p = current['params']

    if p['num_nodes'] <= 20:
        print('  Adjacency list:')
        for node, edges in sorted(graph.items()):
            print(f'    {node}: {edges}')
        print()

    if target is not None:
        print(f'  Shortest path  {source} → {target}')
        print()
        path = dijkstras_algorithm(graph, source=source, target=target)
        result = ' → '.join(str(n) for n in path) if path else 'no path found'
        print(f'  Path   : {result}')
        print()
        print_dijkstras_analytics()
    else:
        print(f'  All shortest paths from node {source}:')
        print()
        dijkstras_algorithm(graph, source=source)
        print_dijkstras_analytics()

    print()
    input('  Press Enter to continue...')


def screen_run_bellman(current, source, target):
    clear()
    header(" RUN BELLMAN-FORD ALGORITHM ")
    if not current:
        print('  No graph selected. Choose or create a graph first.')
        input('  Press Enter to continue...')
        return

    graph = current['graph']
    p = current['params']

    if p['num_nodes'] <= 20:
        print('  Adjacency list:')
        for node, edges in sorted(graph.items()):
            print(f'    {node}: {edges}')
        print()

    try:
        if target is not None:
            print(f'  Shortest path  {source} → {target}')
            print()
            path = bellman_ford_algorithm(graph, source=source, target=target)
            result = ' → '.join(str(n) for n in path) if path else 'no path found'
            print(f'  Path   : {result}')
            print()
            print_bellman_ford_analytics()
        else:
            print(f'  All shortest paths from node {source}:')
            print()
            bellman_ford_algorithm(graph, source=source)
            print_bellman_ford_analytics()
    except ValueError as e:
        print(f'  Error: {e}')

    print()
    input('  Press Enter to continue...')

# main

def main():
    graphs = [{'name': p['name'], 'params': p, 'graph': None} for p in PRESETS]
    current = None
    source = 0
    target = None

    while True:
        print_main_menu(current, source, target)
        choice = input('  Select [1-8]: ').strip()

        if choice == '1':
            result = screen_choose(graphs)
            if result is not None:
                current = result
                source = 0
                target = None

        elif choice == '2':
            graphs, result = screen_create(graphs)
            if result is not None:
                current = result
                source = 0
                target = None

        elif choice == '3':
            source = screen_set_node(current, 'source', source)

        elif choice == '4':
            result = screen_set_node(current, 'target', target)
            target = result

        elif choice == '5':
            screen_selections(current, source, target)

        elif choice == '6':
            screen_run_dijkstras(current, source, target)

        elif choice == '7':
            screen_run_bellman(current, source, target)

        elif choice == '8':
            clear()

        elif choice == '9':
            clear()
            print('  Goodbye.')
            break


if __name__ == '__main__':
    main()
