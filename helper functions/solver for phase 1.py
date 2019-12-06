import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from dijkstra import *

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""
# read file
fp = open('249_200.in')
vertices_num = int(fp.readline())
home_num = int(fp.readline())
vertices = fp.readline()
home = fp.readline()
start = fp.readline()
a = []
for i in range(0, vertices_num):
    temp = fp.readline()
    temp = [x for x in temp.split()]
    a.append(temp)

# make MST, change x to 0
for i in range(0, vertices_num):
    for j in range(0, vertices_num):
        if a[i][j] == 'x':
            a[i][j] = 0
        a[i][j] = float(a[i][j])
X = csr_matrix(a)
Tcsr = minimum_spanning_tree(X)
mst = Tcsr.toarray().astype(float)
for i in range(0, vertices_num):
    for j in range(0, vertices_num):
        if (mst[i][j] != 0):
            mst[j][i] = mst[i][j]
         
vertices = [x for x in vertices.split()]
home = [x for x in home.split()]
start = str(start)[0:3]
start_index = vertices.index(start)
g= Graph() 
gg = g.dijkstra(mst,start_index)
shortestpaths_start = gg[0]
end_index = gg[1]
startToEnd = gg[2]
# make the car's route
output_line1 = []
names_in_path = []
for i in range(0, len(startToEnd)):
    temp = startToEnd[i]
    output_line1.append(vertices[temp])
    names_in_path.append(vertices[temp])
templist = startToEnd[:]
templist.pop()
for i in reversed(templist):
    output_line1.append(vertices[i])

# make stops
homestop = []
for i in home:
    gg = g.dijkstra(mst,vertices.index(i))
    paths = gg[0]
    s = []
    for i in startToEnd:
        s.append(paths[i])
    target_distance = min(s)
    target_vertex_index = paths.index(target_distance)
    homestop.append(target_vertex_index)
stoplines = []
for i in startToEnd:
    temp = []
    temp.append(vertices[i])
    for j in range(0, len(homestop)):
        if homestop[j] == i:
            temp.append(home[j])
    if len(temp) > 1:
        stoplines.append(temp)

output_line2 = len(stoplines)

# print output
for i in output_line1:
    print(i, end = " ")
print()
print(output_line2)
for i in stoplines:
    for j in i:
        print(j, end = " ")
    print()

