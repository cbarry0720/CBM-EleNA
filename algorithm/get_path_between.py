import networkx as nx
import osmnx as ox
import time
import get_elevation

place = 'Amherst, MA'
G = ox.graph_from_place(place)

#path = nx.astar_path(G, nodeToMapFrom, nodeToMapTo, heuristic=dist, weight="cost")
def getPathBetween(G,start, end,k=2):

    start_loc = ox.geocode(start)
    end_loc = ox.geocode(end)

    start_node = ox.nearest_nodes(G,start_loc[1],start_loc[0])
    end_node = ox.nearest_nodes(G,end_loc[1],end_loc[0])
 
    paths = ox.k_shortest_paths(G, start_node,end_node,k)
    K_paths = list(paths)
    print(len(K_paths))
    best_path = []
    best_val = 99999999999
    for path in K_paths:
        dist = 0
        elevation_change = 0
        for i in range(0, len(path)-1):
            node1 = path[i]
            node2 = path[i+1]
            y1 =G.nodes[node1]['y']
            x1 =G.nodes[node1]['x']

            y2 =G.nodes[node2]['y']
            x2 =G.nodes[node2]['x']

            dist += ox.distance.euclidean_dist_vec(y1,x1,y2,x2)
            a_elevation = get_elevation.get_elevation(y1,x1)
            b_elevation = get_elevation.get_elevation(y2,x2)
            elevation_change += a_elevation + b_elevation
        if dist+elevation_change < best_val:
            best_val = dist+elevation_change
            best_path = path
    return best_path

path = getPathBetween(G, "Spoke Amherst", "Stackers Pub Amherst",1)

print(path)
newGraph = nx.subgraph(G, path)
fig, ax = ox.plot_graph(newGraph, figsize=(17,17))

# def getPath(G, start_node, end_node, max_dist_mult):
   