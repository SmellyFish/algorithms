"""This will compute shortest distances between two vertices using Dijkstra's shortest path algorithm."""
__author__ = 'Nikita Makeyev<nikita@nikitamakeyev.com>'
import random


# Setup the graph representation
def setup_graph(file_name, start_vertex):
    graph = {}
    lines = [line.strip().rstrip('\r\n').split('\t') for line in open(file_name)]

    for line in lines:
        edges = {}
        # Figure out all of the edges this vertex had, their destination vertex and the weight
        for i in line[1:]:
            edge_data = i.split(',')
            edges[int(edge_data[0])] = int(edge_data[1])

        # Keep track of this vertex' edges and current shortest distance from origin
        vertex = {'edges': edges}
        if int(line[0]) == start_vertex:
            vertex['has_been_assimilated'] = True
            vertex['distance_from_origin'] = 0
        else:
            vertex['has_been_assimilated'] = False
            vertex['distance_from_origin'] = -1
        graph[int(line[0])] = vertex
    return graph


# Main function
def calc_shortest_paths(graph, debug):
    source_vertex, destination_vertex = find_shortest_edge(graph, debug)
    if not source_vertex == -1:
        if debug:
            print "Next shortest path is from %d to %d." % (source_vertex, destination_vertex)
        assimilate_edge(source_vertex, destination_vertex, graph, debug)
        calc_shortest_paths(graph, debug)

    return graph


# Find shortest edge
def find_shortest_edge(graph, debug):
    found_an_edge = False
    shortest_edge = {'source_vertex': -1, 'destination_vertex': -1}
    shortest_path_weight_found = -1

    for i in graph:
        vertex = graph[i]
        if vertex['has_been_assimilated']:
            for edge_destination_vertex in vertex['edges']:
                if not graph[edge_destination_vertex]['has_been_assimilated']:
                    destination_vertex_distance = calculate_distance_from_origin(i, edge_destination_vertex, graph)
                    if not found_an_edge or destination_vertex_distance < shortest_path_weight_found:
                        shortest_path_weight_found = destination_vertex_distance
                        shortest_edge['source_vertex'] = i
                        shortest_edge['destination_vertex'] = edge_destination_vertex
                        found_an_edge = True

    return shortest_edge['source_vertex'], shortest_edge['destination_vertex']


# Assimilate a new verex
def assimilate_edge(source_vertex, destination_vertex, graph, debug):
    graph[destination_vertex]['has_been_assimilated'] = True
    graph[destination_vertex]['distance_from_origin'] = calculate_distance_from_origin(source_vertex, destination_vertex, graph)


def printVertexSummary(graph, vertices):
    output = ""
    for i in vertices:
        output += str(graph[i]['distance_from_origin']) + ","
    print output


# Calculate a vertex' destination from origin
def calculate_distance_from_origin(source_vertex, destination_vertex, graph):
    return graph[source_vertex]['distance_from_origin'] + graph[source_vertex]['edges'][destination_vertex]


# Toggle between test and real data
if 1:
    graph = setup_graph('dijkstraData.txt', 1)
    graph = calc_shortest_paths(graph, True)
    printVertexSummary(graph, [7, 37, 59, 82, 99, 115, 133, 165, 188, 197])
else:
    graph = setup_graph('testDijkstra3.txt', 13)
    graph = calc_shortest_paths(graph, True)
    printVertexSummary(graph, [5])
