from manim import *

# manim -pql scenes.py BFS
import generator
import algos
from config import * 

class BFS(Scene):
	def construct(self):
		
		# generated graph settings
		n = 15	# number of nodes
		p = .7	# probability of removing an edge
		
		# manim graph settings
		labels = True
		layout = "circular"
		layout_scale = 3

		generated_graph = generator.random_planar_graph(n, p)
		V = generated_graph.all_vertices()
		E = generated_graph.all_edges()

		manim_graph = Graph(V, E, labels=labels, layout=layout, layout_scale=layout_scale)	

		# init all manim node and edge colors
		curr_vc = {}
		curr_ec = {}
		for v in V:
			curr_vc[v] = {"fill_color": state_colors[GraphState.DEFAULT]}
		for e in E:
			curr_ec[e] = {"stroke_color": state_colors[GraphState.DEFAULT]}	
		curr_vc[generated_graph.get_start()] = {"fill_color": state_colors[GraphState.START]}
		curr_vc[generated_graph.get_end()] = {"fill_color": state_colors[GraphState.END]}

		# generate an ordered list of animation state change tuples
		states = algos.bfs_states(generated_graph)

		self.play(Create(manim_graph), run_time=2)

		# animate the algorithm steps
		for s in states:
			vc, ec = s

			# apply state changes
			for k in vc.keys():
				curr_vc[k] = vc[k][k]
			for k in ec.keys():
				curr_ec[k] = ec[k][k]

			# render an animation state
			next_graph = Graph(V, E, labels=labels, layout=layout, layout_scale=layout_scale, vertex_config=curr_vc, edge_config=curr_ec)
			self.play(ReplacementTransform(manim_graph, next_graph))
			manim_graph = next_graph

		self.play(Uncreate(manim_graph), run_time=2)
		self.wait(2)

	# possibly implement tear_down() method
	# which is run when a scene ends
	# maybe save position of graph and use it as a
	# starting position for another rendering?
	# maybe signal the driver program (multi process/threading)
