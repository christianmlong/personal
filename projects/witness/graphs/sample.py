import networkx as nx
import matplotlib.pyplot as plt






def main():
    """
    Main function.
    """
    # args = parse_arguments()
    run_it()

def run_it():
    """
    Run the process.
    """
    g = nx.read_adjlist('puzzle1.graph')

    nx.set_node_attributes(g, 'absences', 0)
    nx.set_edge_attributes(g, 'absences', 0)




    tried = []

    # while true:
    #     l = list(nx.shortest_simple_paths(g, 'm', 'i'))
    #     longest = l[-1]

    l = list(nx.shortest_simple_paths(g, 'm', 'i'))
    l = list(
        single_source_dijkstra_for_graph_with_weighted_nodes_and_edges(
            g,
            source='m',
            target='i',
            weight='absences',
        )
    )
    longest = l[-1]

    print("Success")

def single_source_dijkstra_for_graph_with_weighted_nodes_and_edges(G, source, target=None, cutoff=None, weight='weight'):
    """Compute shortest paths and lengths in a weighted graph G.

    Unlike the regular Dijkstra's algorithm, this version accounts for node
    weight as well as edge weight. It does so by defining a new function to
    calculate edge weight. It then runs the regular Dijkstra's algorithm using
    the new edge weight function.

    Uses Dijkstra's algorithm for shortest paths.

    Parameters
    ----------
    G : NetworkX graph

    source : node label
       Starting node for path

    target : node label, optional
       Ending node for path

    cutoff : integer or float, optional
       Depth to stop the search. Only paths of length <= cutoff are returned.

    Returns
    -------
    distance,path : dictionaries
       Returns a tuple of two dictionaries keyed by node.
       The first dictionary stores distance from the source.
       The second stores the path from the source to that node.


    Examples
    --------
    >>> G=nx.path_graph(5)
    >>> length,path=nx.single_source_dijkstra(G,0)
    >>> print(length[4])
    4
    >>> print(length)
    {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    >>> path[4]
    [0, 1, 2, 3, 4]

    Notes
    -----
    Edge and node weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed, plus weighted
    nodes visited.

    Based on the Python cookbook recipe (119466) at
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119466

    Also see
    https://stackoverflow.com/questions/10453053/graph-shortest-path-with-vertex-weight

    This algorithm is not guaranteed to work if edge weights
    are negative or are floating point numbers
    (overflows and roundoff errors can cause problems).

    See Also
    --------
    single_source_dijkstra_path()
    single_source_dijkstra_path_length()
    """
    if source == target:
        return ({source: 0}, {source: [source]})

    assert not G.is_multigraph()

    def get_weight_for_edge_and_node(u, v, edge_data):
        # The value the user passed for the "weight" label (in the weight
        # parameter) gets captured here in this nested function (closure).
        edge_weight = edge_data.get(weight, 1)

        import pdb; pdb.set_trace()
        # We only care about the weight of the destination node, not the source
        # node. We already paid the cost of getting to the source node, on the
        # last iteration.
        destination_node_weight = v.get(weight, 1)

        return edge_weight + destination_node_weight

    paths = {source: [source]}  # dictionary of paths
    return nx.algorithms.shortest_paths.weighted._dijkstra(
        G,
        source,
        get_weight_for_edge_and_node,
        paths=paths,
        cutoff=cutoff,
        target=target,
    )

def parse_arguments():
    """
    Parse command line. Return arguments.
    """
    argument_parser = argparse.ArgumentParser(
        'Utility to .\n\n'
    )
    argument_parser.add_argument('-a',
                                 '--argument-a',
                                 dest='argument_a',
                                 help=('Argument A: '
                                      ),
                                )
    argument_parser.add_argument('-b',
                                 '--argument-b',
                                 dest='argument_b',
                                 help=('Argument B: '
                                      ),
                                )
    args = argument_parser.parse_args()
    return args

if __name__ == '__main__':
    main()

