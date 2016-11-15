'''
breadth-first search
'''
from collections import deque
#from test_set import GRAPH3 as graph
def bfs_visited(ugraph, start_node):
    '''
    use bfs to visited all the node that can be visited from start_node
    return a set
    '''
    visited = set([start_node])
    queue = deque([start_node])

    while len(queue) > 0:
        node = queue.popleft()
        for neighor in ugraph[node]:
            if neighor not in visited:
                visited.add(neighor)
                queue.append(neighor)
    return visited

def cc_visited(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list of sets,
    where each set consists of all the nodes (and nothing else) in a connected component,
    and there is exactly one set in the list for each connected component in ugraph and nothing else.
    '''
    remain_node = set(ugraph.keys())
    connected_component = []
    while len(remain_node) > 0:
        node = remain_node.pop()
        connected_set = bfs_visited(ugraph,node)
        connected_component.append(connected_set)
        remain_node = remain_node - connected_set
    return connected_component

def largest_cc_size(ugraph):
    '''
    compute the largest size joint in ugraph
    '''
    component_list = cc_visited(ugraph)
    max_size = 0
    for component in component_list:
        if len(component) > max_size:
            max_size = len(component)
    return max_size
def compute_resilience(ugraph, attack_order):
    '''
    Takes the undirected graph ugraph, a list of nodes attack_order and iterates through the nodes in attack_order
    '''
    resilience_order = []
    resilience_order.append(largest_cc_size(ugraph))
    for node in attack_order:
        around = ugraph.pop(node)
        for key in around:
            ugraph[key].remove(node)
        resilience_order.append(largest_cc_size(ugraph))
    return resilience_order
