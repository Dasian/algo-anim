from random import random
from itertools import combinations
import graph
import node

# n is number of nodes
# p is probability of adding edges
# returns a graph object
def random_graph(n=-1, p=.25,isDirected=False):
    if n < 0:
        return None
    
    # set of vertice indices/names
    V = set([v for v in range(n)])

    # set of edge connections
    # (this_node, connected_node)
    E = set()

    # Generate random edges
    for combination in combinations(V, 2):
        a = random()
        if a < p:
            E.add(combination)

    # Create graph
    g = graph.Graph()
    for v in V:
        vertex = node.Node(name=str(v))
        g.add_vertex(vertex)
    for e in E:
        g.add_edge(e)

    # assign start and end nodes

    return g


# driver

# generate random graph(s)
print("Randomly Generated Graph (n=10)")
print(random_graph(n=10))

# call graph algo

# generating/loading async stuff
# constant loop
# full screen animation
# animation queues 