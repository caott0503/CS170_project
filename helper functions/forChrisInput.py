from dijkstra import *



def chrisInput(mat, points):
    output = []
    for i in range(0, len(mat)):
        temp = []
        for j in range(0, len(mat)):
            temp.append(float("inf"))
        output.append(temp)
    for i in range(0, len(points)):
        g = Graph()
        gg = g.dijkstra(graph,points[i])
        j = i
        while (j < len(points)):
            listToAdd = gg[points[j]]
            for i in range(0, len(listToAdd)-1):
        	    if (output[listToAdd[i]][listToAdd[i+1]] == float("inf")):
        		    output[listToAdd[i]][listToAdd[i+1]] = mat[listToAdd[i]][listToAdd[i+1]]
        		    output[listToAdd[i+1]][listToAdd[i]] = output[listToAdd[i]][listToAdd[i+1]]
            j+=1
    indexes = []
    for i in range(0, len(mat)):
        temp = output[i]
        for j in temp:
    	    if (j != float("inf")):
    	        indexes.append(i)
    	        break
    no_indexes=[]
    for i in range(0, len(mat)):
        if i not in indexes:
            no_indexes.append(i)
    for i in output:
    	for j in sorted(no_indexes, reverse=True):
            del i[j]
    for i in sorted(no_indexes, reverse=True):
        del output[i]
    for i in range(0, len(output)):
        output[i][i] = 0

    return [output, indexes]

#example:
graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0], 
        [4, 0, 8, 0, 0, 0, 0, 11, 0], 
        [0, 8, 0, 7, 0, 4, 0, 0, 2], 
        [0, 0, 7, 0, 9, 14, 0, 0, 0], 
        [0, 0, 0, 9, 0, 10, 0, 0, 0], 
        [0, 0, 4, 14, 10, 0, 2, 0, 0], 
        [0, 0, 0, 0, 0, 2, 0, 1, 6], 
        [8, 11, 0, 0, 0, 0, 1, 0, 7], 
        [0, 0, 2, 0, 0, 0, 6, 7, 0] 
        ] 
points = [2,3,7,8]
xxx = chrisInput(graph, points);
for i in range(0, len(xxx[0])):
    print(chrisInput(graph, points)[0][i])
print(chrisInput(graph, points)[1])


