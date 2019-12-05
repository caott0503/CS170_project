import networkx as nx
import numpy as np
from sklearn import cluster
import dijkstra
import itertools
import copy

def decimal_digits_check(number):
    number = str(number)
    parts = number.split('.')
    if len(parts) == 1:
        return True
    else:
        return len(parts[1]) <= 5


def data_parser(input_data):
    number_of_locations = int(input_data[0][0])
    number_of_houses = int(input_data[1][0])
    list_of_locations = input_data[2]
    list_of_houses = input_data[3]
    starting_location = input_data[4][0]

    adjacency_matrix = [[entry if entry == 'x' else float(entry) for entry in row] for row in input_data[5:]]
    return number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix


def adjacency_matrix_to_graph(adjacency_matrix):
    node_weights = [adjacency_matrix[i][i] for i in range(len(adjacency_matrix))]
    adjacency_matrix_formatted = [[0 if entry == 'x' else entry for entry in row] for row in adjacency_matrix]

    for i in range(len(adjacency_matrix_formatted)):
        adjacency_matrix_formatted[i][i] = 0

    G = nx.convert_matrix.from_numpy_matrix(np.matrix(adjacency_matrix_formatted))

    message = ''

    for node, datadict in G.nodes.items():
        if node_weights[node] != 'x':
            message += 'The location {} has a road to itself. This is not allowed.\n'.format(node)
        datadict['weight'] = node_weights[node]

    return G, message


def is_metric(G):
    shortest = dict(nx.floyd_warshall(G))
    for u, v, datadict in G.edges(data=True):
        if abs(shortest[u][v] - datadict['weight']) >= 0.00001:
            return False
    return True


def adjacency_matrix_to_edge_list(adjacency_matrix):
    edge_list = []
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[0])):
            if adjacency_matrix[i][j] == 1:
                edge_list.append((i, j))
    return edge_list


def is_valid_walk(G, closed_walk):
    if len(closed_walk) == 2:
        return closed_walk[0] == closed_walk[1]
    return all([(closed_walk[i], closed_walk[i+1]) in G.edges for i in range(len(closed_walk) - 1)])


def get_edges_from_path(path):
    return [(path[i], path[i+1]) for i in range(len(path) - 1)]


def cost_of_solution(G, car_cycle, dropoff_mapping):
    """
    G is the adjacency matrix.
    car_cycle is the cycle of the car in terms of indices.
    drop-off_mapping is a dictionary of drop-off location to list of TAs that got off at said drop-off location
    in terms of indices.
    """
    cost = 0
    message = ''
    dropoffs = dropoff_mapping.keys()
    if not is_valid_walk(G, car_cycle):
        message += 'This is not a valid walk for the given graph.\n'
        cost = 'infinite'

    if not car_cycle[0] == car_cycle[-1]:
        message += 'The start and end vertices are not the same.\n'
        cost = 'infinite'
    if cost != 'infinite':
        if len(car_cycle) == 1:
            car_cycle = []
        else:
            car_cycle = get_edges_from_path(car_cycle[:-1]) + [(car_cycle[-2], car_cycle[-1])]
        if len(car_cycle) != 1:
            driving_cost = sum([G.edges[e]['weight'] for e in car_cycle]) * 2 / 3
        else:
            driving_cost = 0
        walking_cost = 0
        shortest = dict(nx.floyd_warshall(G))

        for drop_location in dropoffs:
            for house in dropoff_mapping[drop_location]:
                walking_cost += shortest[drop_location][house]

        message += f'The driving cost of your solution is {driving_cost}.\n'
        message += f'The walking cost of your solution is {walking_cost}.\n'
        cost = driving_cost + walking_cost

    message += f'The total cost of your solution is {cost}.\n'
    return cost, message


def convert_locations_to_indices(list_to_convert, list_of_locations):
    return [list_of_locations.index(name) if name in list_of_locations else None for name in list_to_convert]


def convert_matrix(adjMatrix):
    """
    Convert 'x' into 0 if it is the vertice itself, INF if there is no edge.
    """
    numVertices = len(adjMatrix)
    newMatrix = copy.deepcopy(adjMatrix)

    for i in range(numVertices):
        for j in range(numVertices):
            if adjMatrix[i][j] == 'x' and i == j:
                newMatrix[i][j] = 0
            elif adjMatrix[i][j] == 'x' and i != j:
                newMatrix[i][j] = float('inf')
    return newMatrix


def shortestDist_matrix(adjMatrix):
    """
    Floyd-Warshall Algorithm.
    Return an adjacency matrix where each entry is the length of the shortest path between two vertices.
    """
    numVertices = len(adjMatrix)
    newMatrix = copy.deepcopy(adjMatrix)

    for k in range(numVertices):
        for i in range(numVertices):
            for j in range(numVertices):
                newMatrix[i][j] = min(newMatrix[i][j], newMatrix[i][k] + newMatrix[k][j])
    return newMatrix


def shortestDist(adjMatrix, index1, index2):
    """
    Return the length of the shortest path between two vertices with index1 and index2.
    """
    return shortestDist_matrix(adjMatrix)[index1][index2]


def shortestPaths(adjMatrix, start):
    """
    Return the all shortest paths from a starting vertex.
    """
    g = dijkstra.Graph()
    paths = g.dijkstra(adjMatrix, start)
    return paths


def shortestPath(adjMatrix, start, end):
    """
    Return the shortest path between two vertices with index1 and index2.
    """
    for path in shortestPaths(adjMatrix, start):
        if path[-1] == end:
            return path


def hierarchical(locations, shortestDistMatrix, numCluster):
    """
    Use Hierarchical clustering to return a list where each element is a list of points in the clustering
    """
    group = cluster.AgglomerativeClustering(n_clusters=numCluster, affinity='precomputed', linkage='average',
                                            distance_threshold=None).fit(shortestDistMatrix).labels_
    splitLength = []
    for i in range(numCluster):
        splitLength.append(list(group).count(i))
    clustering = [locations[x - y: x] for x, y in zip(itertools.accumulate(splitLength), splitLength)]
    return clustering


def hierarchical_threshold(locations, shortestDistMatrix, threshold):
    """
    Use Hierarchical clustering (with distance threshold) to return a list where
    each element is a list of points in the clustering.
    """
    group = cluster.AgglomerativeClustering(n_clusters=None, affinity='precomputed', compute_full_tree=True,
                                            linkage='average',
                                            distance_threshold=threshold).fit(shortestDistMatrix).labels_
    splitLength = []
    for i in range(len(set(group))):
        splitLength.append(list(group).count(i))
    clustering = [locations[x - y: x] for x, y in zip(itertools.accumulate(splitLength), splitLength)]
    return clustering


def chooseVertice(shortestDistMatrix, clustersIndex, homes, start):
    """
    Choose a vertex index from each cluster so that it minimizes the distance to homes in each cluster.
    """
    vertices = []
    for cluster in clustersIndex:
        if start in cluster:
            vertices.append(cluster[cluster.index(start)])
            continue
        homes_in_cluster = []
        for point in cluster:
            if point in homes:
                homes_in_cluster.append(point)
        distances = []
        for point in cluster:
            distance = 0
            for home in homes_in_cluster:
                distance += shortestDistMatrix[point][home]
            distances.append(distance)
        vertices.append(cluster[distances.index(min(distances))])
    return vertices


def chrisInput_withVerticesInPath(matrix, vertices):
    """
    Create a new pairwise shortest path matrix given vertices.
    """
    output = []
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix)):
            temp.append(float("inf"))
        output.append(temp)

    for i in range(len(vertices)):
        paths = shortestPaths(matrix, vertices[i])
        j = i
        while j < len(vertices):
            listToAdd = paths[vertices[j]]
            for k in range(len(listToAdd) - 1):
                if output[listToAdd[k]][listToAdd[k + 1]] == float("inf"):
                    output[listToAdd[k]][listToAdd[k + 1]] = matrix[listToAdd[k]][listToAdd[k + 1]]
                    output[listToAdd[k + 1]][listToAdd[k]] = output[listToAdd[k]][listToAdd[k + 1]]
            j += 1

    indexes = []
    for i in range(len(matrix)):
        temp = output[i]
        for j in temp:
            if j != float("inf"):
                indexes.append(i)
                break

    no_indexes = []
    for i in range(len(matrix)):
        if i not in indexes:
            no_indexes.append(i)
    for i in output:
        for j in sorted(no_indexes, reverse=True):
            del i[j]
    for i in sorted(no_indexes, reverse=True):
        del output[i]
    for i in range(0, len(output)):
        output[i][i] = 0

    return output, indexes


def chrisInput_onlySelectedVertices(matrix, vertices):
    """
    Create a shortest
    """
    output = shortestDist_matrix(matrix)
    indexes = vertices
    no_indexes = []
    for i in range(len(matrix)):
        if i not in indexes:
            no_indexes.append(i)
    for i in output:
        for j in sorted(no_indexes, reverse=True):
            del i[j]
    for i in sorted(no_indexes, reverse=True):
        del output[i]
    return output


