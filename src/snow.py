import collections
import osmnx as ox
import networkx as nx
from networkx import DiGraph, Graph
from random import choice


def odd_v(g):
    node_list = [vertex for vertex, deg in g.degree() if deg % 2 == 1]
    return node_list


def complete_path_two_nodes(g, vertex1, vertex2):
    shortest = nx.dijkstra_path(g, vertex1, vertex2)
    for i in range(len(shortest) - 1):
        e = g.get_edge_data(shortest[i], shortest[i + 1])[0]
        g.add_edge(shortest[i], shortest[i + 1], length=e["length"])


def length_two_nodes(g, vertex1, vertex2):
    return nx.dijkstra_path_length(g, vertex1, vertex2)


def duplicated_edges_graph(g):
    new_graph = Graph()
    odd_nodes = odd_v(g)
    for n in odd_nodes:
        new_graph.add_node(n)
    for i in range(len(odd_nodes) - 1):
        for j in range(i + 1, len(odd_nodes)):
            new_graph.add_edge(odd_nodes[i], odd_nodes[j], length=length_two_nodes(g, odd_nodes[i], odd_nodes[j]))
    return nx.min_weight_matching(new_graph, True, "length")


def to_eulerian_graph(g):
    duplicates = duplicated_edges_graph(g)
    for dup in duplicates:
        complete_path_two_nodes(g, dup[0], dup[1])


def round_digraph(g):
    new_graph = DiGraph()
    for n1, n2, data in g.edges(data=True):
        new_graph.add_edge(n1, n2, length=round(data["length"]))
    return new_graph


# DENEIGEUSE


def add_for_directed(g):
    fCost, fDict = nx.network_simplex(g, weight="length")
    new_graph = nx.MultiDiGraph(g)
    for k, v in fDict.items():
        for s_key, s_value in v.items():
            for i in range(s_value):
                shortest_path = nx.shortest_path(g, s_key, k, weight="length")
                for j in range(len(shortest_path) - 1):
                    new_graph.add_edge(shortest_path[j], shortest_path[j + 1], length=g.get_edge_data(shortest_path[j], shortest_path[j + 1])["length"])
    for n1 in new_graph.nodes():
        del new_graph.nodes[n1]["demand"]
    return new_graph


def add_demand(g):
    node_dict = dict()
    for n in g.nodes():
        node_dict[n] = g.in_degree(n) - g.out_degree(n)
    nx.set_node_attributes(g, node_dict, "demand")


def demand_count(g):
    c = 0
    for demand in g.nodes.data("demand"):
        if demand[1] != 0:
            c += 1
    return c


place = "Le Kremlin-Bicêtre, France"
start_digraph: DiGraph = ox.graph_from_place(place, network_type='drive')
digraph = start_digraph.copy()
graph: Graph = digraph.to_undirected()
ox.plot_graph(start_digraph)

print("### DRONE ###")
print("Nombre de sommets de degré impair : ", len(odd_v(graph)))
print("Nombre de routes avant duplication : ", len(graph.edges.data("length")))
print("Eulerianisation du graphe...")
to_eulerian_graph(graph)
print("Nombre de routes après duplication : ", len(graph.edges.data("length")))

start = choice(list(graph.nodes))
print("Choix aléatoire du point de départ : ", start)
try:
    circuit = nx.eulerian_circuit(graph, start)
    f_drone = open("drone_path.txt", "w")
    for edge in circuit:
        f_drone.write(','.join(map(str, edge)) + '\n')
    f_drone.close()
except nx.NetworkXError:
    print("Graph isn't eulerian")

print("### DENEIGEUSE ###")

print("Suppression des routes ne faisant pas parti du plus grand graphe fortement connexe")
largest = max(nx.strongly_connected_components(digraph), key=len)
for node in start_digraph.nodes():
    if node not in largest:
        digraph.remove_node(node)
ox.plot_graph(digraph)

print("Is strongly connected ?", nx.is_strongly_connected(digraph))
# Set node attribute "demand"

digraph = round_digraph(digraph)
add_demand(digraph)
print("Nombre de demande : ", demand_count(digraph))
print("Egalisation...")
digraph = add_for_directed(digraph)
print("Is strongly connected ?", nx.is_strongly_connected(digraph))
euler_circuit = list(nx.eulerian_circuit(digraph))
f_snow = open("snow_path.txt", "w")
for road in euler_circuit:
    f_snow.write(','.join(map(str, road)) + '\n')
f_snow.close()

# Format print : noeud1, noeud2, distance
