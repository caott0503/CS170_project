from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
fp = open("demo.in")
vertices_num = int(fp.readline())
home_num = int(fp.readline())
vertices = fp.readline()
home = fp.readline()
start = fp.readline()
a = []
for i in range(0, vertices_num):
	temp = fp.readline()
	temp = [int(x) for x in temp.split()]
	a.append(temp)



X = csr_matrix(a)
Tcsr = minimum_spanning_tree(X)
mst = Tcsr.toarray().astype(int)
print(mst[0][1])
