import string
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

numLocations = 200
numHomes = 99
numEdges = 12500


""" Generate name of all possible locations. """
def nameGenerator(nameLength):
    return [''.join(x) for x in itertools.product(string.ascii_lowercase, repeat=nameLength)]


""" Randomly choose name of positions. """
def randomVertex(n):
    locations = set()
    while len(locations) != n:
        names = nameGenerator(3)
        locations.add(np.random.choice(names))
    return list(locations)


""" Randomly assign coordinate for each position. """
def randomPos():
    return (1000 * np.random.rand(), 1000 * np.random.rand())


def distance(u, v):
    return round(np.sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2), 5)


""" Generate the graph. """
def graphGenerator(l, h, e):
    locations = randomVertex(l)
    pos = [randomPos() for _ in range(l)]
    start = np.random.choice(locations)
    homes = list(np.random.choice(locations, size=h, replace=False))

    graph = nx.Graph()
    for i in range(l):
        graph.add_node(locations[i], pos=pos[i])
    j = 0
    while j < e:
        u = np.random.choice(locations)
        v = np.random.choice(locations)
        if u != v and (u, v) not in graph.edges():
            graph.add_edge(u, v)
            j += 1

    positions = nx.get_node_attributes(graph, 'pos')
    for (u, v) in graph.edges():
        graph.edges[u, v]['weight'] = distance(positions[u], positions[v])

    adjMatrix = nx.to_numpy_matrix(graph)

    """ Output file. """
    with open(str(numLocations) + '.in', 'w+') as f:
        f.write(str(numLocations) + '\n')
        f.write(str(numHomes) + '\n')
        f.write(' '.join(locations) + '\n')
        f.write(' '.join(homes) + '\n')
        f.write(start + '\n')
        for row in np.ndarray.tolist(adjMatrix):
            strRow = [str(i) if i != 0 else 'x' for i in row]
            f.write(' '.join(strRow) + '\n')

    # nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()


if __name__ == '__main__':
    graphGenerator(numLocations, numHomes, numEdges)
