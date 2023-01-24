"""
    Breadth First Search
    Takes as input 
    - a graph
    - start node
    - goal node
    Changes node state for animation

    Implement the algorithm
    Print out the steps
    Print out the results
    Conenct to animation driver
"""

# takes as input the custom graph object
# returns the shortest path from start to end
# as an ordered list
def bfs(graph):
  # init queue
  queue = []
  start = graph.get_start()
  start.visit()
  queue.append(start)

  # debug node and edge processing count
  # tracks num animations done on each obj type
  node_cnt = 0
  edge_cnt = 0

  while queue:
    
    # show which node's edges will be checked
    m = queue.pop(0)
    m.start_work()
    node_cnt += 1
    # show the shortest path to this node
    curr = m.parent
    if curr != None:
      m.start_edge_work(curr)
    while curr != None:
      node_cnt += 1
      edge_cnt += 1
      if curr.parent != None:
        curr.start_edge_work(curr.parent)
      curr.start_work()
      curr = curr.parent

    # process all neighbors of dequeued node
    for neighbor in m.edges:

      # visit edge
      # work on edge
      edge_cnt += 2
      m.visit_edge(neighbor)
      m.start_edge_work(neighbor)

      # process unvisited node
      if neighbor.visited is False:

        # show which node is being checked for end
        neighbor.visit()
        neighbor.start_work()
        neighbor.parent = m
        node_cnt += 2
        
        # found
        if neighbor.isEnd:
          path = []
          curr = neighbor
          while curr != None:
            # retrieve shortest path
            path.append(curr.name)

            # mark the shortest path
            # found node
            curr.found()
            node_cnt += 1
            # found edge
            edge_cnt += 1
            if curr.parent != None:
              curr.found_edge(curr.parent)

            curr = curr.parent

          # statistic debug 
          print("Node Animations: ",node_cnt)
          print("Edge Animations: ", edge_cnt)

          return path[::-1]
        # not found
        else:
          queue.append(neighbor)
          neighbor.end_work() 
          node_cnt += 1
          # end work on edge
          edge_cnt += 1
          neighbor.end_edge_work(m)
    
    # show this path is done
    m.end_work()
    if m.parent != None:
      m.end_edge_work(m.parent)
    curr = m.parent
    while curr != None:
      curr.end_work()
      if curr.parent != None:
        curr.end_edge_work(curr.parent)
      curr = curr.parent
      node_cnt += 1
      edge_cnt += 1

def bfs(V, E, start, end, isDirected):
	"""
		Returns the shortest path from start to end using bfs
		V is list of nodes
		E is list of (start, end) tuples
		Returns [start, ... , end]
	"""
	# create graph dict
	g = {}
	for v in V:
		g[v] = []
	for e in E:
		tmp = g[e[0]]
		tmp.append(e[1])
		g[e[0]] = tmp

  # init queue
	queue = [start]
	visited = [False for i in range(len(V))]  
	parent = [-1 for i in range(len(V))]
	dist = [0 for i in range(len(V))]
	path = []

	while queue:
		curr = queue.pop(0)
		visited[curr] = True
		for neighbor in g[curr]:
			if not visited[neighbor]:
				queue.append(neighbor)
				parent[neighbor] = curr
				dist[neighbor] = dist[parent[neighbor]] + 1
				visited[neighbor] = True
				if neighbor == end:
					p = end 
					while p != -1:
						path.append(p) 
						p = parent[p]
					return path[::-1]

def isConnected(V, E, isDirected):
	"""
		Returns True if a graph is connected
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
		if num_visited == len(V) - 1:
			return True
		for neighbor in g[curr]:
			if not visited[neighbor]:
				queue.append(neighbor)

	return False
