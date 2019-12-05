# This code is contributed by Neelam Yadav and Zian Yan


class Graph:
  
    def minDistance(self,dist,queue):
        minimum = float("Inf")
        min_index = -1

        for i in range(len(dist)):
            if dist[i] < minimum and i in queue: 
                minimum = dist[i] 
                min_index = i 
        return min_index 
  

    def printPath(self, parent, j, l):
          
        if parent[j] == -1 :
            l.append(j)
            return l
        
        self.printPath(parent , parent[j], l) 
        l.append(j)

    def printSolution(self, dist, parent): 
        src = 0
        '''print("Vertex \t\tDistance from Source\tPath")
        for i in range(1, len(dist)): 
            print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, i, dist[i])),
            self.printPath(parent,i)'''
        return dist

    def dijkstra(self, graph, src):
        """
        Function that implements Dijkstra's single source shortest path
        algorithm for a graph represented using adjacency matrix representation
        """
  
        row = len(graph) 
        col = len(graph[0]) 
        dist = [float("Inf")] * row

        parent = [-1] * row 

        dist[src] = 0

        queue = [] 
        for i in range(row): 
            queue.append(i) 

        while queue:
            u = self.minDistance(dist,queue)
            queue.remove(u) 

            for i in range(col):
                if graph[u][i] and i in queue: 
                    if dist[u] + graph[u][i] < dist[i]: 
                        dist[i] = dist[u] + graph[u][i] 
                        parent[i] = u 

        paths = self.printSolution(dist,parent)
        max_path = paths.index(max(paths))
        temp_list = []
        path_to_max = self.printPath(parent, max_path, temp_list)
        all_paths = []
        for i in range(0, len(dist)):
            tl = []
            self.printPath(parent, i, tl)
            all_paths.append(tl)
        return paths, max_path, temp_list, all_paths

