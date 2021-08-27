import osmnx as ox
import networkx as nx
from networkx import MultiDiGraph, MultiGraph

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


print("Liste des sommets de degré impair : ", odd_v(G_projected))
print("Plus court chemin entre noeud 1812939356 et 1613798843 : ", nx.dijkstra_path(graph, 1812939356, 1613798843))
print("Liste des routes avant duplication : ", graph.edges.data("length"))
print("Duplication du plus court chemin entre noeud 1812939356 et 1613798843...")
complete_path_two_nodes(graph, 1812939356, 1613798843)
print("Liste des routes après duplication : ", graph.edges.data("length"))
