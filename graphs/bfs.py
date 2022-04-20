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


def bfs(graph):
  # init queue
  queue = []
  start = graph.get_start()
  start.visit()
  queue.append(start)

  # debug node and edge processing count
  # tracks num animations done on each obj type
  node_cnt = 0
  edge_cnt = 0

  while queue:
    
    # show which node's edges will be checked
    m = queue.pop(0)
    m.start_work()
    node_cnt += 1
    # show the shortest path to this node
    curr = m.parent
    if curr != None:
      m.start_edge_work(curr)
    while curr != None:
      node_cnt += 1
      edge_cnt += 1
      if curr.parent != None:
        curr.start_edge_work(curr.parent)
      curr.start_work()
      curr = curr.parent

    # process all neighbors of dequeued node
    for neighbor in m.edges:

      # visit edge
      # work on edge
      edge_cnt += 2
      m.visit_edge(neighbor)
      m.start_edge_work(neighbor)

      # process unvisited node
      if neighbor.visited is False:

        # show which node is being checked for end
        neighbor.visit()
        neighbor.start_work()
        neighbor.parent = m
        node_cnt += 2
        
        # found
        if neighbor.isEnd:
          path = []
          curr = neighbor
          while curr != None:
            # retrieve shortest path
            path.append(curr.name)

            # mark the shortest path
            # found node
            curr.found()
            node_cnt += 1
            # found edge
            edge_cnt += 1
            if curr.parent != None:
              curr.found_edge(curr.parent)

            curr = curr.parent

          # statistic debug 
          print("Node Animations: ",node_cnt)
          print("Edge Animations: ", edge_cnt)

          return path[::-1]
        # not found
        else:
          queue.append(neighbor)
          neighbor.end_work() 
          node_cnt += 1
          # end work on edge
          edge_cnt += 1
          neighbor.end_edge_work(m)
    
    # show this path is done
    m.end_work()
    if m.parent != None:
      m.end_edge_work(m.parent)
    curr = m.parent
    while curr != None:
      curr.end_work()
      if curr.parent != None:
        curr.end_edge_work(curr.parent)
      curr = curr.parent
      node_cnt += 1
      edge_cnt += 1

