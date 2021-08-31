import collections
import osmnx as ox
import networkx as nx
from networkx import MultiDiGraph, MultiGraph, Graph
from random import choice

place = "Semerville, France"
digraph: MultiDiGraph = ox.graph_from_place(place, network_type='drive')
graph: MultiGraph = digraph.to_undirected()
G_projected = ox.project_graph(graph)


def odd_v(g):
    node_list = [vertex for vertex, deg in g.degree() if deg % 2 == 1]
    return node_list


def complete_path_two_nodes(g, vertex1, vertex2):
    shortest = nx.dijkstra_path(g, vertex1, vertex2)
    for i in range(len(shortest) - 1):
        edge = g.get_edge_data(shortest[i], shortest[i + 1])[0]
        g.add_edge(shortest[i], shortest[i + 1], length=edge["length"])


def length_two_nodes(g, vertex1, vertex2):
    return nx.dijkstra_path_length(g, vertex1, vertex2)


def duplicated_edges_graph(g):
    new_graph = Graph()
    odd_nodes = odd_v(g)
    for node in odd_nodes:
        new_graph.add_node(node)
    for i in range(len(odd_nodes) - 1):
        for j in range(i + 1, len(odd_nodes)):
            new_graph.add_edge(odd_nodes[i], odd_nodes[j], length=length_two_nodes(g, odd_nodes[i], odd_nodes[j]))
    return nx.min_weight_matching(new_graph, True, "length")


def to_eulerian_graph(g):
    duplicates = duplicated_edges_graph(g)
    for dup in duplicates:
        complete_path_two_nodes(g, dup[0], dup[1])


print("Liste des sommets de degré impair : ", odd_v(G_projected))
print("Matching : ", duplicated_edges_graph(graph))
print("Plus court chemin entre noeud 1812939356 et 1613798843 : ", nx.dijkstra_path(graph, 1812939356, 1613798843))
print("Liste des routes avant duplication : ", graph.edges.data("length"))
print("Eulerianisation du graphe...")
to_eulerian_graph(graph)
print("Liste des routes après duplication : ", graph.edges.data("length"))

repeats = [
    item
    for item, count in collections.Counter(graph.edges.data("length")).items()
    if count == 2
]
print("Routes dupliqués : ", repeats)
start = choice(list(graph.nodes))
try:
    circuit = nx.eulerian_circuit(graph, start)
    print("Routes à prendre : ")
    for edge in circuit:
        print(edge)
except nx.NetworkXError:
    print("Graph isn't eulerian")

# Format print : noeud1, noeud2, distance