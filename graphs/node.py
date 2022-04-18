"""
    Graph node class

Attributes (mostly used by animation driver):
    name (str)
    weight (int)
    visited (boolean)
    state (start, goal, working)
    - when goal is reached, all working should change color
    edges (list)
    - in and out edges if graph is undirected
    - only out edges if graph is directed
    - graph object has a flag

TODO:
- Deal with self loops?
"""

class Node:
    def __init__(self, name="noname", weight=None, state="default", visited=False, edges=None):
        self.name = name
        self.weight = weight
        self.state = state
        self.visited = visited
        self.edges = []
        self.isStart = False
        self.isEnd = False

    def visit(self):
        self.visited = True

    def work(self):
        if self.state != "start" and self.state != "goal":
            self.state = "working"

    def set_start(self):
        self.state = 'start'
        self.isStart = True
    
    def set_end(self):
        self.state = 'end'
        self.isEnd = True

    # adds an edge between this node and the supplied node
    # updates the target node if the graph isn't directed
    def add_edge(self, node=None, isDirected=False):
        if node is None or node in self.edges:
            return False
        self.edges.append(node)
        if not isDirected:
            return node.add_edge(self, True)
        return True

    # adds a list of edges (nodes)
    def add_edges(self, nodes=None, isDirected=False):
        for node in nodes:
            self.add_edge(node, isDirected)
        
    def __str__(self):
        
        s = "Name: " + str(self.name) +" weight: "+ str(self.weight) + " state: "+ str(self.state) + " visited: " + str(self.visited)
        s += " Edges: ["
        for e in self.edges:
            s += e.name + ', '
        s = s[0: len(s) - 2]
        s += ']'
        return s 