"""
	Generates custom graph objects (see graph.py)

	Supported graphs:
		Randomly created edges
		Random planar (no crossing edges)
"""
from itertools import combinations
from graph import *
import random

def random_graph(n=-1, p=.05 ,isDirected=False):
	"""
		Generates a random connected graph 
		
		n is number of nodes
		p is probability of adding edges
		returns custom graph obj (graph.py)
	"""
	if n < 2:
		raise("Random graph generation needs at least 2 nodes to assign start and end")
	
	# init
	V = [v for v in range(n)]
	E = []

	# assign start and end nodes
	start = random.randint(0, n-1)
	end = random.randint(0, n-1)
	while end == start: end = random.randint(0, n-1)

	# randomy connect the graph (guarantees path btwn start and end)
	visited = []
	unvisited = [x for x in range(n)]
	curr = unvisited.pop(random.randint(0, n-1))
	while len(visited) < n:
		visited.append(curr)
		adj = unvisited.pop(random.randint(0, len(visited)-1))
		E.append((curr, adj))
		curr = adj

	# Generate random edges
	for combination in combinations(V, 2):
		a = random.random()
		if a < p and combination not in E:
			E.append(combination)

	# put generated graph into custom graph data structure
	g = Graph(V, E, start, end, isDirected)
	return g

def random_planar_graph(n=-1, p=.05, isDirected=False):
	""" 
		Generates a random connected planar graph (no crossing edges)
		
		n is number of nodes
		p is probability of losing edges
		returns custom graph obj (graph.py)
	"""
	if n < 3:
		raise('Planar graph generation requires at least 3 nodes')

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
			if isConnected(V, E, isDirected):
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

	# place values into custom graph object
	g = Graph(V, E, start, end, isDirected)
	return g

def isConnected(V, E, isDirected=False):
	"""
		Returns True if a graph is connected

		V is a list of vertices (ints)
		E is a list of edges/vertice tuples (vert1, vert2)
	"""
	# create graph dict
	g = {}
	for v in V:
		g[v] = []
	for e in E:
		tmp = g[e[0]]
		tmp.append(e[1])
		g[e[0]] = tmp

	# init
	visited = [False for x in range(len(V))]
	queue = [V[0]]
	num_visited = 0

	# bfs and count visited nodes
	while queue:
		curr = queue.pop(0)
		visited[curr] = True
		num_visited += 1
		if num_visited == len(V):
			return True
		for neighbor in g[curr]:
			if not visited[neighbor] and neighbor not in queue:
				queue.append(neighbor)

	return False
