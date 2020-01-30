# project-fa19
Vehicle Routing Planning

### How to run?
```bash
python solver.py --all inputs
```
or
```bash
python3 solver.py --all inputs
```

### FINAL REPORT

General approach:

We want to choose some points as places we must visit, and then transform them into a metric tsp. 
To begin with, we first cluster all the locations into k clusters, based on their distance. In all these k clusters, we determine if every cluster contains home. If one cluster do not contain any homes, then delete the cluster form the list of clusters. Then, randomly pick one point from every cluster that contains home and form a list of place_must_visit. For every pair of vertices in the place_must_visit, find the shortest path, and generate the shortest_distances_matrix of place_must_visit, using the shortest path distance. Because we find the shortest path for each pair, the shortest_distances_matrix is the distance matrix for a complete graph G’.
Then we can solve tsp on G’. We try to use Christofides algorithm for G’, and then rearrange the sequence of the return list, sequence_of_place_must_visit, to make the starting point at first and other relative position the same, obtaining list correct_sequence of pace must visit. Starting from the first location, l1 (starting point), in correct_sequence, add the shortest path of l1, and l2 into list tour. For location li, in correct_sequence, skip it if it has already been visited in tour to avoid unnecessary repeated visiting(e.g. calculate the shortest path of li-1, li+1,). Then get the final tour of car as list tour. At last, for each stop, go back to the certain cluster, and drop the people whose home belongs to that certain cluster. Then get the dictionary of dropoff_home mapping.

Things to consider:

The first thing is that, the number of clusters, k, we want may affect the result. We iterate over different number of cluster for every input, and return the path that yields the smallest energy cost.
We want to use 3opt, which is an improved version of christofides, but it leads to slower processing.
In the process of running over inputs, we notice that some inputs basically have all locations on a line with barely cycles. The 3opt attempt perform especially bad on such inputs. We try to distinguish among these graph, and use 3opt for general random inputs, and use christofides for linear graph, graph with small edge/vertice ratio.

