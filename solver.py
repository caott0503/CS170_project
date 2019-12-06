import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import acopy
import christofides

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""


def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    numLocations = len(list_of_locations)
    numHomes = len(list_of_homes)
    matrix = convert_matrix(adjacency_matrix)
    spMatrix = shortestDist_matrix(matrix)
    graph = adjacency_matrix_to_graph(matrix)[0]
    starting_index = list_of_locations.index(starting_car_location)

    lower = int(numHomes / 2)
    upper = numHomes + 1
    cost = float('inf')
    finalPath = []
    dropoffLocations = {}
    # threshold = numHomes

    home_index = []
    for i in range(numLocations):
        if list_of_locations[i] in list_of_homes:
            home_index.append(i)

    for numCluster in range(lower, upper):
        clustering = hierarchical(list_of_locations, spMatrix, numCluster)
        clustering_index = []
        for c in clustering:
            temp = []
            for vertex in c:
                temp.append(list_of_locations.index(vertex))
            clustering_index.append(temp)

        clusteringIndex = copy.deepcopy(clustering_index)
        for c in clustering_index:
            home_count = 0
            for vertex in c:
                if vertex in home_index:
                    home_count += 1
            if home_count == 0:
                clusteringIndex.remove(c)

        dropOffs = chooseVertice(spMatrix, clusteringIndex, home_index, starting_index)
        newSPMatrix = chrisInput_onlySelectedVertices(matrix, dropOffs)

        SPMatrix_graph = np.array(newSPMatrix)
        # SPMatrix_graph = adjacency_matrix_to_graph(newSPMatrix)[0]

        Path = christofides.christofides_tsp(SPMatrix_graph, starting_node=starting_index)
        realPath = []
        for i in Path:
            realPath.append(dropOffs[i])

        validPath = add_vertices_to_result(realPath, matrix)
        dropoff_Loc = homesInEachCluster(clusteringIndex, home_index)
        locations = {}

        for i in validPath:
            if i in set(dropOffs):
                locations[i] = dropoff_Loc[dropOffs.index(i)]

        # for location, homes in dropoffLocations.items():
        #     location = list_of_locations[location]
        #     for home in homes:
        #         home = list_of_locations[home]
        #
        # for i in finalPath:
        #     i = list_of_locations[i]
        #
        # print(finalPath_index)
        # print(dropoff_Locations_index)

        temp = cost_of_solution(graph, validPath, locations)[0]
        if temp < cost:
            cost = temp
            finalPath = validPath
            dropoffLocations = locations

    return finalPath, dropoffLocations


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
