import osmnx as ox
from networkx import MultiDiGraph, MultiGraph, generate_edgelist

print("hello")

place = "Semerville, France"
digraph: MultiDiGraph = ox.graph_from_place(place, network_type='drive')
graph: MultiGraph = digraph.to_undirected()
G_projected = ox.project_graph(graph)


def odd_v(g):
    node_list = [vertex for vertex, deg in g.degree() if deg % 2 == 1]
    return node_list


print(odd_v(G_projected))




