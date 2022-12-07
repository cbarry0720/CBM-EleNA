import networkx as nx
import osmnx as ox
import time
import get_elevation

place = 'Amherst, MA'
G = ox.graph_from_place(place)

# This method takes the starting graph, a start and end location name and a paramenter for number of shortest paths to find
def getPathBetween(G,start, end,k=2):
    #get the gecode location for the start and end location
    start_loc = ox.geocode(start)
    end_loc = ox.geocode(end)

    #get the nearest node in the grapgh of amherst to the ask locations
    start_node = ox.nearest_nodes(G,start_loc[1],start_loc[0])
    end_node = ox.nearest_nodes(G,end_loc[1],end_loc[0])
    
    #get the k shortest paths from start location to end location
    paths = ox.k_shortest_paths(G, start_node,end_node,k)

    K_paths = list(paths)
    best_path = []
    best_val = 99999999999
    best_dist = 0
    best_elevation = 0
    #for every path returned calculate the distance and total elevation change then return shortest path with smallest changes
    for path in K_paths:
        dist = 0
        elevation_change = 0
        
        for i in range(0, len(path)-1):
            node1 = path[i]
            node2 = path[i+1]
            #Get lat and long of nodes
            y1 =G.nodes[node1]['y']
            x1 =G.nodes[node1]['x']

            y2 =G.nodes[node2]['y']
            x2 =G.nodes[node2]['x']

            dist += ox.distance.euclidean_dist_vec(y1,x1,y2,x2)

            a_elevation = get_elevation.get_elevation(y1,x1) 
            b_elevation = get_elevation.get_elevation(y2,x2)

            elevation_change += abs(a_elevation - b_elevation)

        if dist+elevation_change < best_val:
            best_val = dist+elevation_change
            best_dist = dist
            best_elevation = elevation_change
            best_path = path
    return best_path, best_dist, best_elevation

   