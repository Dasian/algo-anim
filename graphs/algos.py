"""
	Collection of graph algorithms

	Implemented: BFS
	Planned: DFS, Djikstra

	TODO:
"""
import graph as Graph

# TODO
# generates an ordered list of 
# vertex_config and edge_config
# states for every bfs algorithm step
# returns [(vertex_config, edge_config), ...]
# for a manim graph object
def bfs_states(V, E, start, end, isDirected=False):
  # init
	graph = Graph(V, E, start, end, isDirected)
	queue = []
	graph.add_anim_state({GraphState.Visit: [start]})# keep this? part of init
	graph.visit(start)
  queue.append(start)

  # debug node and edge processing count
  # tracks num animations done on each obj type
  node_cnt = 0
  edge_cnt = 0

  while queue:
    
    # show which node is being processed
    m = queue.pop(0)
		graph.add_anim_state({GraphState.PROCESS: [m]})	
    node_cnt += 1
	
    # show current working path
		# might have a bug since a path isn't changed
		# back to visited when it's not part of the
		# process path anymore
		process_path = []
    curr = m.parent
    if curr != None:
			process_path.append(curr, m)
    while curr != None:
      node_cnt += 1
      edge_cnt += 1
      if curr.parent != None:
				process_path.append((graph.get_parent(curr), curr))
			process_path.append(curr)
      curr = graph.get_parent(curr)
		if len(process_path) != 0:
			updates = {GraphState.PROCESS: process_path}
			graph.add_anim_state(updates)

    # process all neighbors of dequeued node
		# put neighbors in Graph or Node obj?
    for neighbor in graph.edges(m):

      # visit edge
      # work on edge
			# TODO figure out what i want here
      edge_cnt += 1
			graph.add_anim_state({GraphState.QUEUED: [(m, neighbor)]})

      # process unvisited node
      if graph.is_visited(neighbor) is False:

        # show which node is being checked for end
				# a check state?
				graph.add_anim_state({GraphState.PROCESS: [neighbor]})
				graph.set_parent(neighbor, m)
        node_cnt += 1
        
        # found
        if graph.get_end() == neighbor:
          path = []
					anim_path = []
          curr = neighbor
          while curr != None:
            # retrieve shortest path
            path.append(curr)

            # mark the shortest path
            # found node
						anim_path.append(curr)
            graph.update_node(curr, GraphState.FOUND)
            node_cnt += 1
            # found edge
            edge_cnt += 1
            if curr.parent != None:
							anim_path.append(curr.parent, curr)
              graph.update_edge(curr, curr.parent, GraphState.FOUND)

            curr = graph.get_parent(curr)

          # statistic debug 
          print("Node Animations: ", node_cnt)
          print("Edge Animations: ", edge_cnt)

					update = {GraphState.FOUND: anim_path}
					graph.add_anim_state(update)	
          return graph.anim_states()

        # not found
        else:
          queue.append(neighbor)
          graph.update_node(neighbor, GraphState.VISIT) 
          node_cnt += 1
          # end work on edge
          edge_cnt += 1
          graph.update_edge(neighbor, m, GraphState.VISIT)
    
    # show this path is done
    graph.end_work(m)
    if m.parent != None:
      graph.end_edge_work(m, m.parent)
    curr = m.parent
    while curr != None:
      graph.end_work(curr)
      if curr.parent != None:
        graph.end_edge_work(curr, curr.parent)
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
