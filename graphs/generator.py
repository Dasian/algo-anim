from itertools import combinations
import graph
import node as gnode
import random
import algos

# n is number of nodes
# p is probability of adding edges
# returns custom graph object
# TODO guarantee the graph is planar
def random_graph(n=-1, p=.05 ,isDirected=False):
    
    # need to assign distinct start and end nodes
    if n < 2:
        return None

    # maybe set p to be 1/n^c
    p = 1/n
    
    # set of vertices indices/names
    V = [v for v in range(n)]

    # set of edge connections
    # (this_node, connected_node)
    E = []

    # randomly connect all vertices
    # (guarantees a path between start and end)
    initialSet = [v for v in range(n)]
    visitedSet = []
    curVertex = initialSet.pop(random.randrange(len(initialSet)))
    visitedSet.append(curVertex)

    # loop through all the vertices, connecting them randomly
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

    # put generated graph into custom graph data structure
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
    while end == start: end = random.randint(0, n-1)
    g.get_vertice(str(start)).set_start()
    g.set_start(g.get_vertice(str(start)))
    g.get_vertice(str(end)).set_end()

    return g

def random_planar_graph(n=-1, p=.05, isDirected=False):
	""" Generates a random planar graph with n nodes, prob p of losing edges"""
	if n < 3:
		return None

	# start with K3 graph and a list of faces
	# (a face is a group of nodes)
	# init the face queue with the first inner face (K3)
	V = [0, 1, 2]
	E = [(0,1), (1,0), (1,2), (2,1), (2,0), (0,2)]
	F = [(0, 1, 2)]

	# add a node in a face then add the 3 new faces to the queue 
	while len(V) < n:
		face = F.pop(0)
		newVert = len(V)
		V.append(newVert)
		for i in range(len(face)):
			e = face[i]
			E.append((newVert, e))
			E.append((e, newVert)) # makes things work, graph direction
			F.append((e, newVert, face[(i+1)%len(face)]))

	# assign start and end nodes
	global start
	global end
	start = random.randint(0, n-1)
	end = random.randint(0, n-1)
	while end == start: end = random.randint(0, n-1)

	# remove random edges
	# ensure a path from start to end exists (connected)
	i = 0
	while i < len(E):
		# remove edge if it keeps the graph connected
		if random.random() < p:
			tmp = E.pop(i)
			tmp2 = None
			# remove duplicate
			if not isDirected:
				tmp2 = E.pop(i)
			if algos.isConnected(V, E, isDirected):
				i -= 2
			else:
				# removal causes disconnect, put it back!!
				E.insert(i, tmp)
				if not isDirected:
					E.insert(i+1, tmp2)
		if isDirected:
			i += 1
		else:
			i += 2

	return V, E	

def main():
	# TODO add cmd flags

    # generate random graph(s)
    n = 25
    print("Randomly Generated Graph (n="+str(n)+")")
    g = random_graph(n)

    # call graph algo
    solution = algos.bfs(graph=g)
    print("Shortest Path: ", solution)

    # generating/loading async stuff
    # constant loop
    # full screen animation
    # animation queues 

if __name__ == '__main__':
    main()
