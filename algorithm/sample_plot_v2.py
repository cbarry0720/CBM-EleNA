import networkx as nx
import osmnx as ox
import time


place = 'Amherst, MA'
G = ox.graph_from_place(place)

#path = nx.astar_path(G, nodeToMapFrom, nodeToMapTo, heuristic=dist, weight="cost")
def getPathBetween(G,location1, location2):
    nodeToMapToTup = ox.geocode(location1)
    nodeToMapFromTup = ox.geocode(location2)

    node1 = ox.nearest_nodes(G,nodeToMapFromTup[1],nodeToMapFromTup[0])
    node2 = ox.nearest_nodes(G,nodeToMapToTup[1],nodeToMapToTup[0])
    print(node1)
    print(node2)
    return nx.shortest_path(G,node1,node2)
path = getPathBetween(G, "Spoke Amherst", "Umass Amherst")

print(path)
newGraph = nx.subgraph(G, path)
fig, ax = ox.plot_graph(newGraph, figsize=(17,17))