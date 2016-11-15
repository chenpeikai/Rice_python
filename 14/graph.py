'''my solutioin'''
EX_GRAPH0 = {0:set([1,2]),1:set([]),2:set([])}
EX_GRAPH1 = {0:set([1,4,5]),1:set([2,6]),2:set([3]),3:set([0]),4:set([1]),5:set([2]),6:set([])}
EX_GRAPH2 = {0:set([1,4,5]),1:set([2,6]),2:set([3,7]),3:set([7]),4:set([1]),5:set([2]),6:set([]),7:set([3]),8:set([1,2]),9:set([0,4,5,6,7,3])}
GRAPH0 = {0: set([1]),
          1: set([2]),
          2: set([3]),
          3: set([0])}

def make_complete_graph(num_nodes):
    '''
    Takes the number of nodes num_nodes and returns a dictionary corresponding to a
     complete directed graph with the specified number of nodes
    '''
    graph = {}
    for index in range(num_nodes):
        temp = set(range(num_nodes))
        temp.remove(index)
        graph[index] = temp
    return graph

def compute_in_degrees(digraph):
    '''
    Takes a directed graph digraph (represented as a dictionary) 
    and computes the in-degrees for the nodes in the graph
    '''
    distributions = {}
    for key,values in digraph.items():
        if not distributions.has_key(key):
            distributions[key] = 0
        for value in values:
            if distributions.has_key(value):
                distributions[value] += 1
            else:
                distributions[value] = 1
    return distributions
        
def in_degree_distribution(digraph):
    '''
    Takes a directed graph digraph (represented as a dictionary) and computes 
    the unnormalized distribution of the in-degrees of the graph
    '''
    distributions = {}
    degrees_dict = compute_in_degrees(digraph)
    for _,values in degrees_dict.items():
        if distributions.has_key(values):
            distributions[values] += 1
        else:
            distributions[values] = 1
    return distributions
