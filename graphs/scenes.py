from manim import *

# manim -pql scenes.py BFS
import generator

class BFS(Scene):
	def construct(self):
		# make a graph
		n = 17 
		V, E = generator.random_planar_graph(n, p=0.3)
		graph = Graph(V, E, labels=True, layout="random", layout_scale=4)	

		# have custom graph/bfs algo return a list of animation steps
		# loop through those steps or something?

		# animate
		self.play(Create(graph), run_time=4)
		self.wait(2)
		self.play(Uncreate(graph), run_time=4)
		self.wait(2)

	# possibly implement tear_down() method
	# which is run when a scene ends
	# maybe save position of graph and use it as a
	# starting position for another rendering?
	# maybe signal the driver program (multi process/threading)
