from manim import *

# manim -pql scenes.py BFS
import generator

class BFS(Scene):
	def construct(self):
		# generate a graph
		n = 5
		V, E = generator.random_planar_graph(n, p=0.3)
		graph = Graph(V, E, labels=True, layout="random", layout_scale=4)	

		# create all animation states
		# init all node and edge colors
		curr_vc = {}
		curr_ec = {}
		for v in V:
			curr_vc[v] = {"fill_color": GREY}
		for e in E:
			curr_ec[e] = {"stroke_color": GREY}	
		# generate an ordered list of state change tuples
		render_queue = []
		states = algos.bfs_states(V, E)
		for s in states:
			vc, ec = s

			# apply state changes
			for k in vc.keys():
				curr_vc[k] = vc[k]
			for k in ec.keys():
				curr_ec[k] = ec[k]			

			# maybe actually render here? doesn't need to take up space
			render_queue.append(Graph(V, E, labels=labels, layout=layout, layout_scale=layout_scale, vertex_config=curr_vc, edge_config=curr_ec)

		# render all animation states
		# (possibly render each state when immediately generated?)
		for r in render_queue:
			self.play(r)
		self.play(Create(graph), run_time=4)
		self.wait(2)
		self.play(Uncreate(graph), run_time=4)
		self.wait(2)

	# possibly implement tear_down() method
	# which is run when a scene ends
	# maybe save position of graph and use it as a
	# starting position for another rendering?
	# maybe signal the driver program (multi process/threading)
