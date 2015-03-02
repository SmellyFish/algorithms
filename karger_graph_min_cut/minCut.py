"""This will compute the minimum cut of an undirected graph using Karger's randomized contraction algorithm."""
__author__ = 'Nikita Makeyev<nikita@nikitamakeyev.com>'
import random


# Setup the graph
def setup_graph(file_name):
    # Represent the graph as a dictionary of lists. Each key in the dictionary represents a tail vertex while each
    # value in the dictionary is a list representing all head vertices for that tail vertex
    graph = {}
    lines = [line.strip().rstrip('\r\n').split('\t') for line in open(file_name)]
    for line in lines:
        graph[int(line[0])] = [int(i) for i in line[1:]]
    return graph


# Main function
def calc_min_cut(graph, debug):
    # Keep track of iterations. Unnecessary, used for display reasons.
    iterations = 1
    num_of_vertices = len(graph)

    # Keep contracting until there are only 2 vertices left
    while num_of_vertices > 2:
        print "Running main method iteration %d" % iterations

        num_of_vertices -= 1
        tail_vertex, head_vertex = choose_random_edge(graph)
        if debug:
            print "About to contract edge from %d to %d" % (tail_vertex, head_vertex)
        graph = contract_edge(tail_vertex, head_vertex, graph, debug)
        iterations += 1

    # There should only be 2 vertices left in the graph. The length of their lists should be equal and represent the
    # number of crossing edges
    return len(graph.itervalues().next())


# Choose edge randomly
def choose_random_edge(graph):
    # Grab random tail vertex
    tail_vertex = random.choice(graph.keys())
    # Grab random head vertex
    head_vertex = random.choice(graph[tail_vertex])
    return tail_vertex, head_vertex


# Contract edge. Merge head into tail
def contract_edge(tail_vertex, head_vertex, graph, debug):
    if debug:
        print "BEGIN contract_edge"
    # All the vertices that need to be updated to point to tail instead of head
    edges_to_update = graph[head_vertex]
    # Remove the head vertex since it's being merged into the tail
    del graph[head_vertex]
    # Remove all edges that point from tail to head
    tail_vertex_without_head_edges = []
    for vertex in graph[tail_vertex]:
        if vertex != head_vertex:
            tail_vertex_without_head_edges.append(vertex)
    graph[tail_vertex] = tail_vertex_without_head_edges

    # Update all edges currently pointing to the head vertex to point to tail instead
    for edge_to_update in edges_to_update:
        if debug:
            print "List before contraction: %s" % graph[edge_to_update]
            print "Readjusting edge %d during contraction" % edge_to_update
        # Ignore self loops
        if edge_to_update == tail_vertex:
            if debug:
                print "Self loop detected, skipping"
            continue
        else:
            graph[tail_vertex].append(edge_to_update)
            graph[edge_to_update] = [x if x != head_vertex else tail_vertex for x in graph[edge_to_update]]
        if debug:
            print "List after contraction: %s" % graph[edge_to_update]
    return graph

# APP LOGIC
# Keep track of the smallest min cut
min_cut = -1
# Since the algorithm is a randomized one, we have to run it many times to determine the proper min cut of the graph
for i in range(0, 100):
    # Alternate between test and live graph source files
    if 1:
        graph = setup_graph('kargerMinCut.txt')
    else:
        # graph = setup_graph('testMinCut8.txt')
        graph = setup_graph('testMinCut40.txt')

    next_min_cut = calc_min_cut(graph, False)
    if (min_cut == -1) or (next_min_cut < min_cut):
        min_cut = next_min_cut

print "Minimum Cut is %d" % min_cut