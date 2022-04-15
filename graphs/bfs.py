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

def bfs(visited, graph, start): # function for BFS
  visited.append(start)
  queue.append(start)

  while queue:          # Creating loop to visit each node
    m = queue.pop(0) 
    m.work()
    print (m, end = " ") 

    for neighbour in graph[m]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)
        neighbour.visit()
        neighbour.work()

