import itertools

import numpy as np
import networkx as nx

from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.euler import eulerian_circuit

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from mst_utils import minimal_spanning_tree


def christofides_tsp(graph, starting_node=0):
    """
    Christofides TSP algorithm
    http://www.dtic.mil/dtic/tr/fulltext/u2/a025602.pdf
    Args:
        graph: 2d numpy array matrix
        starting_node: of the TSP
    Returns:
        tour given by christofies TSP algorithm
    Examples:
        >>> import numpy as np
        >>> graph = np.array([[  0, 300, 250, 190, 230],
        >>>                   [300,   0, 230, 330, 150],
        >>>                   [250, 230,   0, 240, 120],
        >>>                   [190, 330, 240,   0, 220],
        >>>                   [230, 150, 120, 220,   0]])
        >>> christofides_tsp(graph)
    """

    mst = minimal_spanning_tree(graph, 'Prim', starting_node=0)

    print(mst)

#    X = csr_matrix(graph_ori)
#    Tcsr = minimum_spanning_tree(X)
#    mst = Tcsr.toarray().astype(float)
#    for i in range(0, len(graph_ori)):
#        for j in range(0, len(graph_ori)):
#            if (mst[i][j] != 0):
#                mst[j][i] = mst[i][j]
#    print(mst)

    odd_degree_nodes = list(_get_odd_degree_vertices(mst))
    odd_degree_nodes_ix = np.ix_(odd_degree_nodes, odd_degree_nodes)
    print(odd_degree_nodes_ix)
    nx_graph = nx.from_numpy_array(-1 * graph[odd_degree_nodes_ix])
    print(-1 * graph[odd_degree_nodes_ix])
    matching = max_weight_matching(nx_graph, maxcardinality=True)
    print(matching)
    euler_multigraph = nx.MultiGraph(mst)
    for edge in matching:
        euler_multigraph.add_edge(odd_degree_nodes[edge[0]], odd_degree_nodes[edge[1]],
                                  weight=graph[odd_degree_nodes[edge[0]]][odd_degree_nodes[edge[1]]])
    euler_tour = list(eulerian_circuit(euler_multigraph, source=starting_node))
    print(euler_tour)
    path = list(itertools.chain.from_iterable(euler_tour))
    return _remove_repeated_vertices(path, starting_node)#[:-1]


def _get_odd_degree_vertices(graph):
    """
    Finds all the odd degree vertices in graph
    Args:
        graph: 2d np array as adj. matrix
    Returns:
    Set of vertices that have odd degree
    """
    odd_degree_vertices = set()
    for index, row in enumerate(graph):
        if len(np.nonzero(row)[0]) % 2 != 0:
            odd_degree_vertices.add(index)
    return odd_degree_vertices


def _remove_repeated_vertices(path, starting_node):
    length = len(path) // 2
    for i in range(0, length):
        if path[i] == path[i+1]:
            path.pop(i)
    path.pop(-1)
    duplicate = [item for item in set(path) if path.count(item) > 1]
    #do not treat the starting point as duplicate
    #duplicate.pop(0)
    print(path)
    for ele in duplicate:
        dupli_index = duplicates_index(path, ele)
        #start when the same element appear the second time
        dupli_index.pop(0)
        print(dupli_index)
        for i in dupli_index:
            if graph[path[i-1]][path[i+1]] != float('inf'):
                path.pop(i)
                dupli_index = [x - 1 for x in dupli_index]
                dupli_index.pop(0)

    path.append(starting_node)
    return path

def duplicates_index(lst, item):
    return [i for i, x in enumerate(lst) if x == item]



#graph_ori = [[  0, 300, 250, 190, 230], [300,   0, 230, 330, 150], [250, 230,   0, 240, 120], [190, 330, 240,   0, 220], [230, 150, 120, 220,   0]]
graph_ori = [[0, 1, 1, 1, float('inf')], [1, 0, 1, float('inf'), 1], [1, 1, 0, float('inf'), 1], [1, float('inf'), float('inf'), 0, 1], [float('inf'), 1, 1, 1, 0]]
print(graph_ori)

graph = np.array(graph_ori)

print(christofides_tsp(graph))
