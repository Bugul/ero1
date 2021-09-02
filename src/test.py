import collections
import osmnx as ox
import networkx as nx
from networkx import MultiDiGraph, MultiGraph, DiGraph, Graph
from random import choice

place = "Semerville, France"
start_digraph: DiGraph = ox.graph_from_place(place, network_type='drive')
digraph = start_digraph.copy()
graph: Graph = digraph.to_undirected()
ox.plot_graph(start_digraph)


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


# DENEIGEUSE

def add_for_directed(g):
    fCost, fDict = nx.network_simplex(g, weight="length")
    new_graph = nx.MultiDiGraph(g)

    for k, v in fDict.items():
        for s_key, s_value in v.items():
            for i in range(s_value[0]):
                shortest_path = nx.shortest_path(g, s_key, k, weight="length")
                for j in range(len(shortest_path) - 1):
                    new_graph.add_edge(shortest_path[j], shortest_path[j + 1], length=g.get_edge_data(shortest_path[j], shortest_path[j + 1])[0]["length"])
    for n1 in new_graph.nodes():
        del new_graph.nodes[n1]["demand"]
    return new_graph


print("### DRONE ###")
print("Liste des sommets de degré impair : ", odd_v(graph))
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

print("### DENEIGEUSE ###")
largest = max(nx.strongly_connected_components(digraph), key=len)
for node in start_digraph.nodes():
    if node not in largest:
        digraph.remove_node(node)
ox.plot_graph(digraph)
print("Is strongly connected ?", nx.is_strongly_connected(digraph))
print(list(nx.strongly_connected_components(digraph)))
for e in digraph.nodes():
    print(e, digraph.in_degree(e) - digraph.out_degree(e))
# Set node attribute "demand"
node_dict = dict()
for n in digraph.nodes():
    node_dict[n] = digraph.in_degree(n) - digraph.out_degree(n)
nx.set_node_attributes(digraph, node_dict, "demand")
print("Demande : ", digraph.nodes.data("demand"))
digraph = add_for_directed(digraph)
euler_circuit = list(nx.eulerian_circuit(digraph))
for road in euler_circuit:
    print(road)

# Format print : noeud1, noeud2, distance
