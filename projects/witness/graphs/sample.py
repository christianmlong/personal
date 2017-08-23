from collections import deque
from heapq import heappush, heappop
from itertools import count

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

    nx.set_node_attributes(g, 'ZZZ', 0)
    print(nx.get_node_attributes(g, 'ZZZ'))
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

        # We only care about the weight of the destination node, not the source
        # node. We already paid the cost of getting to the source node, on the
        # last iteration.
        destination_node_weight = v.get(weight, 1)

        return edge_weight + destination_node_weight

    paths = {source: [source]}  # dictionary of paths
    import pdb; pdb.set_trace()
    return _dijkstra(
        G,
        source,
        get_weight_for_edge_and_node,
        paths=paths,
        cutoff=cutoff,
        target=target,
    )

def _dijkstra(G, source, get_weight, pred=None, paths=None, cutoff=None,
              target=None):
    """Implementation of Dijkstra's algorithm

    Parameters
    ----------
    G : NetworkX graph

    source : node label
       Starting node for path

    get_weight: function
        Function for getting edge weight

    pred: list, optional(default=None)
        List of predecessors of a node

    paths: dict, optional (default=None)
        Path from the source to a target node.

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

    pred,distance : dictionaries
       Returns two dictionaries representing a list of predecessors
       of a node and the distance to each node.

    distance : dictionary
       Dictionary of shortest lengths keyed by target.
    """
    G_succ = G.succ if G.is_directed() else G.adj

    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {source: 0}
    c = count()
    fringe = []  # use heapq with (distance,label) tuples
    push(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        if v == target:
            break

        for u, e in G_succ[v].items():
            cost = get_weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist[v] + get_weight(v, u, e)
            if cutoff is not None:
                if vu_dist > cutoff:
                    continue
            if u in dist:
                if vu_dist < dist[u]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))
                if paths is not None:
                    paths[u] = paths[v] + [u]
                if pred is not None:
                    pred[u] = [v]
            elif vu_dist == seen[u]:
                if pred is not None:
                    pred[u].append(v)

    if paths is not None:
        return (dist, paths)
    if pred is not None:
        return (pred, dist)
    return dist

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

