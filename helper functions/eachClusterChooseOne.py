from student_utils import *
def chooseOne(adj_mat, clusters, homes):
	shortestPathMatrix = shortestDist_matrix(adj_mat)
	output = []
	for cluster in clusters:
		homes_in_cluster = []
		for point in cluster:
			if point in homes:
				homes_in_cluster.append(point)
		distances = []
		for point in cluster:
			distance = 0
			for home in homes_in_cluster:
				distance += shortestPathMatrix[point][home]
			distances.append(distance)
		output.append(cluster[distances.index(min(distances))])
	return output


