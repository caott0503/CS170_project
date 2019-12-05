from student_utils import *

def add_vertices_to_result(path, graph) :
    path_result[]
    path_result_set = set(path_result)
    start_index = 0
    end_index = 1
    while end_index < len(path):
        if path[end_index] in path_result_set:
            end_index += 1
        else:
            path_between_two_points = shortestPath(graph, path[start_index], path[end_index];
            path_result.extend(path_between_two_points[:-1])
            path_result_set = set(path_result);
            start_index += 1
            end_index = start_index + 1
    path_result.append(path[-1])

path_1 = [3,1,4,2]
graph_1 = [[0,1,1,float('inf')], [1,0,1,float('inf')], [1,1,0,1], [float('inf'), float('inf'), 1,0]]
add_vertices_to_result(path_1, graph_1)
