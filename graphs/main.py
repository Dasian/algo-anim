from itertools import combinations
import graph
import node as gnode
import random
import networkx as nx
import matplotlib.pyplot as plt
import bfs

# n is number of nodes
# p is probability of adding edges
# returns a graph object
def random_graph(n=-1, p=.05 ,isDirected=False):
    
    # need to assign distinct start and end nodes
    if n < 2:
        return None

    # maybe set p to be 1/n^c
    p = 1/n
    
    # set of vertice indices/names
    V = set([v for v in range(n)])

    # set of edge connections
    # (this_node, connected_node)
    E = set()

    # randomly connect all vertices
    # (guarantees a path between start and end)
    initialSet = set([v for v in range(n)])
    visitedSet = set()
    curVertex = random.sample(initialSet, 1).pop()
    initialSet.remove(curVertex)
    visitedSet.add(curVertex)
    #loop through all the vertices, connecting them randomly
    while initialSet:
        adjVertex = random.sample(initialSet, 1).pop()
        edge = (curVertex, adjVertex)
        E.add(edge)
        initialSet.remove(adjVertex)
        visitedSet.add(adjVertex)
        curVertex = adjVertex

    # Generate random edges
    for combination in combinations(V, 2):
        a = random.random()
        if a < p and combination not in E:
            E.add(combination)

    # Create graph
    g = graph.Graph(num_nodes=n)
    for v in V:
        vertex = gnode.Node(name=str(v))
        g.add_vertex(vertex)
    for e in E:
        g.add_edge(e)

    # assign start and end nodes
    global start
    global end
    start = random.randint(0, n-1)
    end = random.randint(0, n-1)
    while end == start:
        end = random.randint(0, n-1)
    g.get_vertice(str(start)).set_start()
    g.set_start(g.get_vertice(str(start)))
    g.get_vertice(str(end)).set_end()

    return g


# driver
def main():
    # generate random graph(s)
    n = 100
    print("Randomly Generated Graph (n="+str(n)+")")
    g = random_graph(n)

    # nx graph for printing
    edges = g.generate_edges()
    nx_graph = nx.Graph()
    nx_graph.add_edges_from(edges)

    # color starting and ending node
    color_map = []
    for i in nx_graph.nodes():
        if i == str(start):
            color_map.append('green')
        elif i == str(end):
            color_map.append('red')
        else:
            color_map.append('blue')

    # call graph algo
    solution = bfs.bfs(graph=g)
    print("Shortest Path: ", solution)

    # draw the graph
    plt.figure(3,figsize=(16,16)) 
    nx.draw_random(nx_graph, with_labels = True, node_color=color_map)
    plt.show()

    # generating/loading async stuff
    # constant loop
    # full screen animation
    # animation queues 

if __name__ == '__main__':
    main()