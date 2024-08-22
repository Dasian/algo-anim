"""
	Collection of animated graph algorithms
    Generates a a series of animation states
    that will create a scene.

	Implemented: BFS
	Planned: DFS, Djikstra

	TODO:
"""
from .config import *

def bfs_states(graph):
	"""
		Generates an ordered list of manim vertex_config and edge_config states
		for every bfs step.

		input: generated graph obj (see graph.py)
		returns [(vertex_config, edge_config), ...]
	"""
	# init
	queue = [graph.get_start()]
	prev_path = []

	# BFS TIME BITCHES
	while queue:

		# process next node in the queue
		m = queue.pop(0)	# 0 if bfs, empty if dfs
		graph.visit(m)	

		# generate the current process path
		curr_path = []
		curr = m
		while curr != None:
			curr_path.append(curr)
			parent = graph.get_parent(curr)
			if parent != None:
				curr_path.append((parent, curr))
			curr = parent
		# curr_path is currently in reverse order
		# this fixes it, ordering from start -> m
		curr_path = curr_path[::-1]

		# compare current process path with previous path
		# elements in prev but not in curr will have
		# their states changed to visited
		# note that current path will always be >= prev_path
		path_differences = []
		for i in range(len(prev_path)):
			if prev_path[i] != curr_path[i]:
				path_differences.append(prev_path[i])

		# add the currently processed path as one state
		# note any element in the curr/prev path has already
		# been visited
		if len(curr_path) != 0:
			updates = {
				GraphState.PROCESS: curr_path, 
				GraphState.VISITED: path_differences
			}
			graph.add_anim_state(updates)

		# process all neighbors of dequeued node
		for neighbor in graph.edges(m):

			# check/queue unvisited neighbors
			if graph.is_visited(neighbor) is False and neighbor not in queue:

				# animate check neighbor
				graph.add_anim_state({GraphState.CHECK: [(m, neighbor), neighbor]})
				graph.set_parent(neighbor, m)

				# neighbor is the end bitches
				# animate found path
				if graph.get_end() == neighbor:
					found_path = curr_path
					found_path.append((m, neighbor))
					found_path.append(neighbor)
					updates = {GraphState.FOUND: found_path}
					graph.add_anim_state(updates)	
					return graph.get_anim_states()

				# animate queue neighbor
				queue.append(neighbor)
				graph.add_anim_state({GraphState.QUEUED: [(m, neighbor), neighbor]})

		# neighbor checking is done
		# need to revert changing process path back to the visited state
		# determine the next processing path and compare the changes
		prev_path = curr_path
