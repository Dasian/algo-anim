"""
    Breadth First Search
    Takes as input 
    - a graph
    - start node
    - goal node
    Changes node state for animation

    Implement the algorithm
    Print out the steps
    Print out the results
    Conenct to animation driver
"""

visited = []    # List for visited nodes.
queue = []      # Initialize a queue

# start key
def bfs(graph):
  print(graph)

  start = None

  for i in range(0, graph.get_num_nodes()):
    node = graph.get_vertice(str(i))
    if node.isStart:
      start = node
      print("Start: ", start.name)
      break

  visited.append(start)
  queue.append(start)

  path = ''

  while queue:          # Creating loop to visit each node
    m = queue.pop(0) 
    # m.work()
    # print (m, end = " ") 

    path += '\nVisiting: ' + m.name + '\nNeighbors: '
    m.visit()

    for neighbor in m.edges:
      if neighbor.isEnd:
        m.visit()
        path += neighbor.name + ' '
        print("End: ", neighbor.name)

        print(graph)
        return path
      elif neighbor not in visited:
        path += neighbor.name + ' '
        visited.append(neighbor)
        m.visit()
        queue.append(neighbor)
        #neighbor.work()

