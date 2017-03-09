# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
from collections import deque
from Queue import Queue, PriorityQueue

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    if start == goal:
        return list(start)
    paths = deque([ [ start, node ] for node in graph.get_connected_nodes(start) ])
    while len(paths) != 0:
        path = paths.popleft()
        if path[-1] == goal: 
            return path
        else:
            for node in graph.get_connected_nodes(path[-1]):
                epath = list(path)
                epath.append(node)
                paths.append(epath)
    return []
    

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    if start == goal:
        return list(start)
    
    paths = [ [ start, node ] for node in graph.get_connected_nodes(start) ]
    while len(paths) != 0:
        path = paths.pop()
        if path[-1] == goal: 
            return path
        else:
            for node in graph.get_connected_nodes(path[-1]):
                if path.count(node) == 0:
                    epath = list(path)
                    epath.append(node)
                    paths.append(epath)
    return []


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    if start == goal:
        return list(start)
    
    paths = [ [ start, node ] for node in sorted(graph.get_connected_nodes(start), key=(lambda x: graph.get_heuristic(x, goal)), reverse=True) ]
    while len(paths) != 0:
        path = paths.pop()
        if path[-1] == goal: 
            return path
        else:
            cnodes = sorted(graph.get_connected_nodes(path[-1]), key=(lambda x: graph.get_heuristic(x, goal)), reverse=True)
            for node in cnodes:
                if path.count(node) == 0:
                    epath = list(path)
                    epath.append(node)
                    paths.append(epath)
    return []


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    if start == goal:
        return list(start)
    
    paths = Queue(maxsize=beam_width)
    try:
        for node in sorted(graph.get_connected_nodes(start), key=(lambda x: graph.get_heuristic(x, goal))): paths.put_nowait([ start, node ])
    except:
        pass

    while not paths.empty():
        path = paths.get_nowait()
        if path[-1] == goal: 
            return path
        else:
            cnodes = sorted(graph.get_connected_nodes(path[-1]), key=(lambda x: graph.get_heuristic(x, goal)))
            try:
                for node in cnodes:
                    if path.count(node) == 0:
                        epath = list(path)
                        epath.append(node)
                        paths.put_nowait(epath)
            except:
                pass
    return []


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.
## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    pLength = 0

    for i in range(1, len(node_names)):
        pLength += graph.get_edge(node_names[i-1], node_names[i]).length

    return pLength


def branch_and_bound(graph, start, goal):
    if start == goal:
        return list(start)

    paths = PriorityQueue()
    for node in graph.get_connected_nodes(start): paths.put_nowait((path_length(graph, [ start, node ]), [ start, node ]))

    while not paths.empty():
        path = paths.get_nowait()
        if path[1][-1] == goal: 
            return path[1]
        else:
            cnodes = graph.get_connected_nodes(path[1][-1])
            for node in cnodes:
                if path[1].count(node) == 0:
                    epath = list(path[1])
                    epath.append(node)
                    paths.put_nowait((path_length(graph, epath), epath))
    return []


def a_star(graph, start, goal):
    extendedSet = set()
    if start == goal:
        return list(start)

    paths = PriorityQueue()
    for node in graph.get_connected_nodes(start): paths.put_nowait((path_length(graph, [ start, node ]) + graph.get_heuristic(node, goal), [ start, node ]))
    extendedSet.add(start)

    while not paths.empty():
        path = paths.get_nowait()
        if path[1][-1] == goal: 
            return path[1]
        elif path[1][-1] not in extendedSet:
            extendedSet.add(path[1][-1])
            cnodes = graph.get_connected_nodes(path[1][-1])
            for node in cnodes:
                if path[1].count(node) == 0:
                    epath = list(path[1])
                    epath.append(node)
                    paths.put_nowait((path_length(graph, epath) + graph.get_heuristic(node, goal), epath))
    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    pathList = []
    for node in graph.nodes:
        if node != goal:
            pathList.append(branch_and_bound(graph, node, goal))
    for path in pathList:
        if path_length(graph, path) < graph.get_heuristic(path[0], path[-1]):
            return False
    return True


def is_consistent(graph, goal):
    pathList = []
    for node in graph.nodes:
        if node != goal:
            pathList.append(branch_and_bound(graph, node, goal))
    for path in pathList:
        for cnode in graph.get_connected_nodes(path[0]):
            if abs(graph.get_heuristic(path[0], goal) - graph.get_heuristic(cnode, goal)) > graph.get_edge(path[0], cnode).length:
                return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '8'
WHAT_I_FOUND_INTERESTING = 'All'
WHAT_I_FOUND_BORING = 'None'
