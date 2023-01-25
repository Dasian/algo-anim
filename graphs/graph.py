"""
	Custom Graph class used to track 
	algorithm animation states

	G = {"name": Node}

	TODO:
		add animation state tracking
		add/define custom colors
		update graph methods + attributes
		clean up!
"""

class Graph(object):

    def __init__(self, V, E, start, end, isDirected=False):
		self.start = start
		self.end = end
		self.parents = [None for x in range(len(V))] # parents[vert] = vert.parent
		self.visited = [False for x in range(len(V))] # visited[vert] = vert.isVisited
		self.graph_dict = {}
		self.anim_states = [] # ordered list of (vc, ec)

		# graph_dict[vertice] = [edges]
		for v in V:
			self.graph_dict[v] = [] 
		for e in E:
			tmp = self.graph_dict[e[0]]
			tmp.append(e[1])
			self.graph_dict[e[0]] = tmp

		# this needs to be specified
		self.state_colors = {} # {VISITED: YELLOW}

	def add_anim_state(self, updates):
		"""
			Adds all changes in the updates dictionary as one
			animation state
			This lets you update multiple objects at the same time
			updates = {GraphState.xxx: [Node1, Node2, Edge1, ...], ...}
			edge = (src_node, dest_node)

			updates above is slightly more space efficient than list of tuples
			with a lot of repeating states
		"""
		vc = {}
		ec = {}
		for k in updates.keys():
			for o in updates[k]:
				if type(o) is Node:
					vc[o.id] = {o.id: {"fill_color": self.state_colors[k]}}
				elif type(o) is tuple:
					ec[o] = {o: {"stroke_color": self.state_colors[k]}}
		anim_state = (vc, ec)
		self.anim_states.append(anim_state)

    def set_start(self, start):
        self.start = start

    def get_start(self):
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
        verts = []
        for key in self.graph_dict:
            verts.append(self.graph_dict[key])
        return verts

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
        edges = set()
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex].edges:
                if (neighbour.name, vertex) not in edges:
                    edges.add((vertex, neighbour.name))
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
            res += str(self.graph_dict[key]) + "\n"
        return res
