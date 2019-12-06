import numpy as np

"""
The input parser is written in accordance to the specification at 
https://cs170.org/assets/project/spec.pdf
input:
filename <- str: the name of .in file
output:
numLocations <- int: number of locations in graph
numHomes <- int: number of homes (TAs) in graph
locations <- list<str>: the list of locations
homes <- list<str>: the list of homes
startlocation <- str: the starting point of the problem
graph <- Graph: a data-structure that abstracts the graph problem. * See Graph class below
"""

CAR_COST = 2/3
WALK_COST = 1

def read_input(filename):
    if not filename.endswith('.in'):
        raise FileNotFoundError('the input file need to end with .in')

    with open(filename) as f:
        numLocations = int(f.readline())
        numHomes = int(f.readline())
        locations = f.readline().split()
        homes = f.readline().split()
        startLocation = f.readline().split()[0]

        adjMatrix = []
        for _ in range(numLocations):
            adjMatrix.append(f.readline().split())

        graph = Graph(adjMatrix, locations)

    return numLocations, numHomes, locations, homes, startLocation, graph


"""
Similar to read_intput, this is a handy function that helps parse parameters in the output file
input:
filename <- str: the name of .out file
output:
locVisisted <- list<str>: a list of locations that is visited in order by the car
numDropOff <- int: number of drop-off locations
locDist <- map<str, list<str>>: map location (where people drop off) to a list of locations (dropped-off people's homes)
doctest:
>>> t = read_output("sample/demo1.out")
>>> t
(['Soda', 'Dwinelle', 'Campanile', 'Barrows', 'Soda'], 3, {'Soda': ['Cory'], 'Dwinelle': ['Wheeler', 'RSF'], 'Campanile': ['Campanile']})
"""


def read_output(filename):
    if not filename.endswith('.out'):
        raise FileNotFoundError('the input file need to end with .out')

    with open(filename) as f:
        locVisited = f.readline().split()
        # check that it's a cycle
        if locVisited[0] != locVisited[-1]:
            raise ValueError('the list of locations should form a cycle')
        numDropOff = int(f.readline())

        locDict = dict()
        for i in range(numDropOff):
            line = f.readline().split()
            locDict[line[0]] = line[1:]

    return locVisited, numDropOff, locDict


class Graph(object):
    """
    preprocess the adjacancy list and get an dictionary representation
    """

    def __init__(self, matrix, locNames=None):
        self.pathFlag = False
        self.matrix = matrix
        self.neighbors = dict()

        if locNames:
            self.locNames = dict()
            for index, locName in enumerate(locNames):
                self.locNames[locName] = index

        for index, row in enumerate(self.matrix):
            self.neighbors[index] = [i for i, j in enumerate(row) if j is not 'x']

    """
    DP algorithm which computes pair-wise shortest paths in O(V^3), which
    can be greatly truncated due to the triangular property
    """

    def initializeShortestPath(self):
        # avoid recomputation
        if self.pathFlag:
            return

        length = len(self.matrix)

        self.shortPath = dict()
        for i in range(length):
            self.shortPath[(i, i)] = 0

        indirect = dict()
        for i in range(length - 1):
            indirect[i] = []
            for j in range(i + 1, length):
                if j not in self.neighbors[i]:
                    indirect[i].append(j)
                    self.shortPath[(i, j)] = float('inf')
                else:
                    self.shortPath[(i, j)] = self.length(i, j)

        for k in range(length):
            for i in range(length - 1):
                for j in indirect[i]:
                    if k != i and k != j:
                        tmpDist = self.shortestDist(i, k) + self.shortestDist(k, j)
                        self.shortPath[(i, j)] = min(self.shortPath[(i, j)], tmpDist)

        self.pathFlag = True

    """
    edge length from u to v if there is any edge
    return None if such edge doesn't exist
    """

    def length(self, u, v):
        return float(self.matrix[u][v])

    def getNeighbor(self, u):
        return self.neighbors[u]

    def shortestDist(self, u, v):
        if u < v:
            return self.shortPath[(u, v)]
        else:
            return self.shortPath[(v, u)]

    def shortestDistByName(self, loc1, loc2):
        u = self.locNames[loc1]
        v = self.locNames[loc2]
        return self.shortestDist(u, v)


"""
FIX: This function is already done in the given skeleton code
"""


def evaluate_output(graph, locVisisted, locDict):
    pass


if __name__ == "__main__":
    graph = read_input("sample/demo1.in")[-1]
    graph.initializeShortestPath()

