"""
    Custom Graph class used to track 
    algorithm animation states

    TODO:
        clean up!
        figure out how to store/animate pseudo code instructions
        stuff like visualizing the queue and stuff
"""
from . import config

class Graph(object):

    def __init__(self, V=[], E=[], start=-1, end=-1, isDirected=False):
        self.start = start
        self.end = end
        self.isDirected = isDirected
        self.anim_states = [] # ordered list of (vc, ec)
        self.parents = [None for x in range(len(V))] # parents[vert] = vert.parent
        self.visited = [False for x in range(len(V))] # visited[vert] = vert.isVisited

        # generates a graph from V and E
        # graph_dict[vertice] = [edges]
        self.graph_dict = {}
        for v in V:
            self.graph_dict[v] = []
        for src, dest in E:
            self.graph_dict[src].append(dest)

    def add_anim_state(self, updates):
        """
            Adds all changes in the updates dictionary as one
            animation state
            This lets you update multiple objects at the same time
            updates = {GraphState.xxx: [Node1, Node2, Edge1, ...], ...}
            edge = (src_node, dest_node)
            This also ignores any changes to the start and end nodes

            updates above is slightly more space efficient than list of tuples
            with a lot of repeating states
        """
        vc, ec = {}, {}
        for k in updates.keys():
            for o in updates[k]:
                if type(o) is int and o != self.start and o != self.end:
                    vc[o] = {o: {"fill_color": config.state_colors[k]}}
                elif type(o) is tuple:
                    # manim/networkx maybe doesn't color an edge correctly
                    o = (min(o), max(o))
                    ec[o] = {o: {"stroke_color": config.state_colors[k]}}
        anim_state = (vc, ec)
        self.anim_states.append(anim_state)
        # every state is a tuple of dicts that represent the graph changes
        # for this step

    def get_anim_states(self):
        return self.anim_states

    def set_start(self, start):
        self.start = start

    def get_start(self):
        """ returns the start node; start nodes have their parent set to None """
        return self.start

    def set_end(self, end):
        self.end = end

    def get_end(self):
        return self.end

    def visit(self, node):
        self.visited[node] = True

    def is_visited(self, node):
        return self.visited[node]

    def set_parent(self, node, parent):
        self.parents[node] = parent

    def get_parent(self, node):
        return self.parents[node]

    def edges(self, vertice):
        """ returns a list of all the edges of a vertice"""
        return self.graph_dict[vertice]
        
    def all_vertices(self):
        """ returns the vertices of a graph as a list """
        return self.graph_dict.keys()

    def all_edges(self):
        """ returns the edges of a graph """
        return self.generate_edges()

    def add_vertex(self, vertex):
        """ adds vertex to dict """
        if vertex.name not in self.graph_dict:
            self.graph_dict[vertex.name] = vertex

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        vertex1, vertex2 = tuple(edge)
        self.graph_dict[vertex1].add_edge(node=self.graph_dict[vertex2], isDirected=self.isDirected)

    def generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex]:
                if (neighbour, vertex) not in edges:
                    edges.append((vertex, neighbour))
        return edges
    
    def __iter__(self):
        self._iter_obj = iter(self.graph_dict)
        return self._iter_obj
    
    def __next__(self):
        """ allows us to iterate over the vertices """
        return next(self._iter_obj)

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.generate_edges():
            res += str(edge) + " "
        res += "\nobjects: \n"
        for key in self.graph_dict:
            res += 'key: ' + str(key) + ' value: ' + str(self.graph_dict[key]) + "\n"
        return res
