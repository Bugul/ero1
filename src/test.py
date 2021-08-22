import osmnx as ox
from networkx import MultiDiGraph, MultiGraph

print("hello")

place = "Montréal, Canada"
digraph: MultiDiGraph = ox.graph_from_place(place, network_type='drive')
graph: MultiGraph = digraph.to_undirected()
G_projected = ox.project_graph(graph)
ox.plot_graph(G_projected)
