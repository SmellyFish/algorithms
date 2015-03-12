"""This will compute the sizes of top 5 strongly connected components of a directed graph using Kosaraju's two-pass
algorithm."""
__author__ = 'Nikita Makeyev<nikita@nikitamakeyev.com>'
import operator

# Setup the graph
def setup_graph(file_name):
    graph = {}
    reverse_graph = {}

    lines = [line.strip().rstrip('\r\n').split(' ') for line in open(file_name)]
    for line in lines:
        add_arc_to_graph(graph, int(line[0]), int(line[1]))
        add_arc_to_graph(reverse_graph, int(line[1]), int(line[0]))

    return graph, reverse_graph

# Add an arc to a graph
def add_arc_to_graph(graph, tail_vertex, head_vertex):
    if head_vertex not in graph:
        graph[head_vertex] = []

    if tail_vertex in graph:
        graph[tail_vertex].append(head_vertex)
    else:
        graph[tail_vertex] = [head_vertex]
    return

def generate_new_vertex_meta_data():
    return {'visited_on_first_run': False, 'visited_on_second_run': False, 'leader': -1}

# Run DFS on a graph and record finishing times
def run_finishing_time_dfs(graph, graph_meta_data, start_vertex, debug=False):
    if debug:
        print "Running finishing time DFS on vertex %d" % start_vertex

    if (start_vertex not in graph_meta_data['vertex_data']) or (graph_meta_data['vertex_data'][start_vertex]['visited_on_first_run'] is not True):
        vertex = graph[start_vertex]

        vertex_meta_data = generate_new_vertex_meta_data()
        vertex_meta_data['visited_on_first_run'] = True
        graph_meta_data['vertex_data'][start_vertex] = vertex_meta_data

        for i in vertex:
            if (i not in graph_meta_data['vertex_data']) or (graph_meta_data['vertex_data'][i]['visited_on_first_run'] is not True):
                if debug:
                    print "Recursing into vertex %d" % i
                run_finishing_time_dfs(graph, graph_meta_data, i, debug)
            else:
                if debug:
                    print "Skipping vertex %d" % i

        graph_meta_data['current_finishing_time'] += 1
        graph_meta_data['vertex_finishing_time_map'][graph_meta_data['current_finishing_time']] = start_vertex
    return

# Run DFS on a graph and record finishing times
def run_leader_dfs(graph, graph_meta_data, start_vertex, debug=False):
    if graph_meta_data['vertex_data'][start_vertex]['visited_on_second_run'] is not True:
        vertex = graph[start_vertex]
        graph_meta_data['vertex_data'][start_vertex]['visited_on_second_run'] = True
        graph_meta_data['vertex_data'][start_vertex]['leader'] = graph_meta_data['current_leader']

        for i in vertex:
            if graph_meta_data['vertex_data'][i]['visited_on_second_run'] is not True:
                run_leader_dfs(graph, graph_meta_data, i, debug)
    return

def analyze_leader_data_in_graph_data(graph_meta_data):
    leader_data = {}
    for i in graph_meta_data['vertex_data']:
        vertex_leader = graph_meta_data['vertex_data'][i]['leader']
        if vertex_leader in leader_data:
            leader_data[vertex_leader] += 1
        else:
            leader_data[vertex_leader] = 1
    sorted_leader_data = sorted(leader_data.items(), key=operator.itemgetter(1))

    number_of_leaders_to_return = 5
    if len(sorted_leader_data) < number_of_leaders_to_return:
        return sorted_leader_data
    else:
        return sorted_leader_data[-number_of_leaders_to_return:]

# Main function
def main(graph, reverse_graph, debug=False):
    # Dictionary to keep track of graph & vertex meta data such as finishing time and leader
    graph_meta_data = {'current_finishing_time': 0, 'current_leader': 0, 'vertex_finishing_time_map': {}, 'vertex_data': {}}

    for i in graph:
        # Run first pass DFS on reverse graph to figure out finishing times
        run_finishing_time_dfs(reverse_graph, graph_meta_data, i, debug)

    i = graph_meta_data['current_finishing_time']
    while i > 0:
        next_vertex_index = graph_meta_data['vertex_finishing_time_map'][i]
        graph_meta_data['current_leader'] = next_vertex_index
        run_leader_dfs(graph, graph_meta_data, next_vertex_index, debug)
        i -= 1

    return graph_meta_data

graph, reverse_graph = setup_graph('scc_test2.txt')
graph_meta_data = main(graph, reverse_graph, False)
leader_data = analyze_leader_data_in_graph_data(graph_meta_data)

# print "The graph is %s and the data is: %s" % (reverse_graph, data)
print "Leader data is %s" % (leader_data)
#print "Sample arcs are %s and %s" % (graph[2], graph[10])