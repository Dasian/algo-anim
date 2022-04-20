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
    def __init__(self, name="noname", weight=None, visited=False, edges=None, parent=None):
        self.name = name
        self.weight = weight
        self.visited = visited # if this node has been processed already
        self.edges = [] # list of conected Node objects/vertices
        self.working = False # if this node is being processed
        self.isStart = False
        self.isEnd = False
        self.parent = None # parent node (none for src)
        self.isFound = False # if this node is part of the path
        self.edgeState = {} # key is a Node in edges; Value is state (working, visited, none)
        self.edgeFound = {} # key is edge; value is Boolean if found

    def found(self):
        self.isFound = True

    def found_edge(self, node):
        self.edgeFound.update({node: True})
        self.edgeState.update({node: 'found'})

    def visit(self):
        # make this node yellow
        self.visited = True

    def visit_edge(self, neighbor):
        # make this edge yellow
        self.edgeState.update({neighbor: 'visited'})

    # displays work animation starting at this node ending at the neighbor node
    def start_edge_work(self, neighbor):
        # make this edge working color
        self.edgeState.update({neighbor: 'working'})

    def end_edge_work(self, neighbor):
        # turn the edge back to yellow
        self.edgeState.update({neighbor: 'visited'})    

    def start_work(self):
        # make this node purple or something
        self.working = True
    
    def end_work(self):
        self.working = False

    def set_start(self):
        self.isStart = True
    
    def set_end(self):
        self.isEnd = True

    # adds an edge between this node and the supplied node
    # updates the target node if the graph isn't directed
    def add_edge(self, node=None, isDirected=False):
        if node is None or node in self.edges:
            return False
        self.edges.append(node)
        self.edgeState.update({node: 'default'})
        self.edgeFound.update({node: False})
        if not isDirected:
            return node.add_edge(self, True)
        return True

    # adds a list of edges (nodes)
    def add_edges(self, nodes=None, isDirected=False):
        for node in nodes:
            self.add_edge(node, isDirected)
        
    def __str__(self):
        if self.parent is None:
            parent_name = 'None'
        else:
            parent_name = self.parent.name
        s = "Name: " + str(self.name) + "\n\tisStart:" +str(self.isStart)
        s += "\n\tisEnd: "+str(self.isEnd)+"\n\tweight: "+ str(self.weight) 
        s += "\n\tstate: "+ str(self.state) + " \n\tvisited: " + str(self.visited) 
        s += '\n\tparent: ' + parent_name
        s += '\n\tedgeState: {'+self.edgeState+'}'
        s += "\n\tEdges: ["
        for e in self.edges:
            s += e.name + ', '
        s = s[0: len(s) - 2]
        s += ']'
        return s 