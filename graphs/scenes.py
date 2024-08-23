"""
    Creates a manim scene based on animation
    states generated.
"""

# manim -pql scenes.py BFS
from manim import *
from . import generator
from . import algos
from .config import * 

# generates algo scene for graphs
class GraphScene(Scene):
    def __init__(self, n=5, algo='BFS', height=3, children=2):
        super().__init__()

        # manim graph settings
        self.labels = True
        # circular, bfs_layout with networkx stuff?
        self.layout = "tree"
        self.layout_scale = 5
        self.height = height
        self.children = children

        # algorithm settings
        self.algo = algo.upper()
        # key is algo, value is corresponding animation state function
        self.state_generator = {'BFS': algos.bfs_states,
                                'DFS': algos.dfs_states}

    def construct(self):
        # generate a graph/tree
        generated_graph = generator.balanced_tree(self.children, self.height)
        V = generated_graph.all_vertices()
        E = generated_graph.all_edges()
        manim_graph = Graph(V, E, labels=self.labels, layout=self.layout, layout_scale=self.layout_scale, root_vertex=0)   

        # init node and edge colors
        curr_vc, curr_ec = {}, {}
        for v in V:
            curr_vc[v] = {"fill_color": state_colors[GraphState.DEFAULT]}
        for e in E:
            curr_ec[e] = {"stroke_color": state_colors[GraphState.DEFAULT]} 
        curr_vc[generated_graph.get_start()] = {"fill_color": state_colors[GraphState.START]}
        curr_vc[generated_graph.get_end()] = {"fill_color": state_colors[GraphState.END]}

        # generate an ordered list of animation state change tuples
        # returns generated_graph.get_anim_states()
        states = self.state_generator[self.algo](generated_graph)

        # animate the algorithm steps
        self.play(Create(manim_graph), run_time=2)
        for s in states:
            vc, ec = s

            # what the fuck
            # apply state changes
            for k in vc.keys():
                curr_vc[k] = vc[k][k]
            for k in ec.keys():
                curr_ec[k] = ec[k][k]

            # render one animation state/step
            next_graph = Graph(V, E, root_vertex=0, labels=self.labels, layout=self.layout, layout_scale=self.layout_scale, vertex_config=curr_vc, edge_config=curr_ec)
            self.play(ReplacementTransform(manim_graph, next_graph))
            manim_graph = next_graph

        # destroy graph
        self.wait(2)
        self.play(Uncreate(manim_graph), run_time=2)
        self.wait(2)

    # possibly implement tear_down() method
    # which is run when a scene ends
    # maybe save position of graph and use it as a
    # starting position for another rendering?
    # maybe signal the driver program (multi process/threading)
