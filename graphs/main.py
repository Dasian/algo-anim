from itertools import combinations
import graph
import node as gnode
import random
import matplotlib.pyplot as plt
import networkx as nx
import bfs

max_fig_size = 100

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
    V = [v for v in range(n)]

    # set of edge connections
    # (this_node, connected_node)
    E = []

    # randomly connect all vertices
    # (guarantees a path between start and end)
    initialSet = [v for v in range(n)]
    visitedSet = []

    print("init set", initialSet)
    print(random.randrange(len(initialSet)))

    curVertex = initialSet.pop(random.randrange(len(initialSet)))
    visitedSet.append(curVertex)
    #loop through all the vertices, connecting them randomly
    while initialSet:
        adjVertex = initialSet.pop(random.randrange(len(initialSet)))
        edge = (curVertex, adjVertex)
        E.append(edge)
        visitedSet.append(adjVertex)
        curVertex = adjVertex

    # Generate random edges
    for combination in combinations(V, 2):
        a = random.random()
        if a < p and combination not in E:
            E.append(combination)

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

def animate_random_growth(nx_graph, g, color_map):
    # colors of the animated graph
    color_subset = []
    # draw start and end nodes first
    color_subset.append(color_map[start])
    color_subset.append(color_map[end])
    nx_graph.add_node(str(start), Position=(0, 0))
    nx_graph.add_node(str(end), Position=(max_fig_size, max_fig_size))

    edges = g.generate_edges()
    for edge in edges:
        this, next = edge

        # positioning 
        if this not in nx_graph.nodes:
            nx_graph.add_node(this, Position=(random.randrange(0, max_fig_size), random.randrange(0, max_fig_size)))
            color_subset.append(color_map[int(this)])
        if next not in nx_graph.nodes:
            nx_graph.add_node(next, Position=(random.randrange(0, max_fig_size), random.randrange(0, max_fig_size)))    
            color_subset.append(color_map[int(next)])
        # if (this, next) not in nx_graph.edges
        nx_graph.add_edge(this, next)
        
        # printing
        # color_map will be the global color store
        # pass the subset of the displayed colors
        nx.draw(nx_graph, with_labels=True, pos=nx.get_node_attributes(nx_graph,'Position'), node_color=color_subset)
        plt.pause(.50)

# add new edges if at least one node exists
# edges being drawn is still being worked on
# add new nodes if there is an edge between existing node and new node
def animate_bfs_growth(nx_graph=None, g=None, color_map=None):
    # colors of the animated graph
    color_subset = []
    # draw start and end nodes first
    color_subset.append(color_map[start])
    color_subset.append(color_map[end])
    nx_graph.add_node(str(start), Position=(0, 0))
    nx_graph.add_node(str(end), Position=(max_fig_size, max_fig_size))
    queue = [str(start)]
    visited = []
    edges = []
    while queue:
        curr = queue.pop(0)
        visited.append(curr)
        
        # adding unvisisted nodes and edges
        neighbors = g.get_vertice(curr).edges
        for this in neighbors:
            # track state
            if this.name in visited:

                if (curr, this.name) in edges:
                    continue

                # add edge btween curr and this
                nx_graph.add_edge(curr, this.name)
                edges.append((curr, this.name))
                nx.draw(nx_graph, with_labels=True, pos=nx.get_node_attributes(nx_graph,'Position'), node_color=color_subset)
                plt.pause(.50)
                continue
            visited.append(this.name)
            queue.append(this.name)

            # adding new node and edge
            if int(this.name) != end:
                nx_graph.add_node(this.name, Position=(random.randrange(0, max_fig_size), random.randrange(0, max_fig_size)))
                color_subset.append(color_map[int(this.name)])
                nx_graph.add_edge(curr, this.name)
                edges.append((curr, this.name))
            else: # stop drawing if path to end node is found
                nx_graph.add_edge(curr, this.name)
                edges.append((curr, this.name))
                nx.draw(nx_graph, with_labels=True, pos=nx.get_node_attributes(nx_graph,'Position'), node_color=color_subset)
                return

            # draw current graph state
            nx.draw(nx_graph, with_labels=True, pos=nx.get_node_attributes(nx_graph,'Position'), node_color=color_subset)
            plt.pause(.50)


# driver
def main():
    # generate random graph(s)
    n = 25
    global max_fix_size
    max_fig_size = 100
    print("Randomly Generated Graph (n="+str(n)+")")
    g = random_graph(n)

    # TODO: matploit animation library
    # animate the growth of the entire graph before the algo
    # edge is (srcNode, destNode)
    nx_graph = nx.Graph() 
    plt.figure(1,figsize=(7,7)) 

    # key: value
    # node: color
    # init colors of entire graph (for animations)
    color_map = []
    for i in range(n):
        if i == start:
            color_map.append('green')
        elif i == end:
            color_map.append('red')
        else:
            color_map.append('blue')

    # animate the growth of the graph using bfs
    # stops when a path between the start and end are found
    # doesn't color the path
    # animate_bfs_growth(nx_graph=nx_graph, g=g, color_map=color_map)

    # animate drawing the entire graph randomly
    # animate_random_growth(nx_graph, g, color_map)
    
    # draw the whole graph (no animation)
    nx_graph.add_edges_from(g.all_edges())
    color_map = []
    for i in nx_graph.nodes:
        if i == str(start):
            color_map.append('green')
        elif i == str(end):
            color_map.append('red')
        else:
            color_map.append('blue')
    nx.draw_random(nx_graph, with_labels = True, node_color=color_map)

    # call graph algo
    solution = bfs.bfs(graph=g)
    print("Shortest Path: ", solution)

    # draw the graph
    plt.show()

    # generating/loading async stuff
    # constant loop
    # full screen animation
    # animation queues 

if __name__ == '__main__':
    main()