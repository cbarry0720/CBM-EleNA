import osmnx as ox
import sys
class get_path_between:
    __start_loc = None
    __end_loc = None
    __G = None
    
    def __init__(self, start_loc, end_loc, G):
        self.__start_loc = ox.geocode(start_loc)
        self.__end_loc = ox.geocode(end_loc)
        self.__G = G

    def get_location_node(self,loc):
        return ox.nearest_nodes(self.__G, loc[1], loc[0])

    def get_k_shortest_paths(self, k):
        return ox.k_shortest_paths(self.__G, self.__start_loc,self.__end_loc, k)
    
    def get_node_longitiude(node):
        return node['x']

    def get_node_latitude(node):
        return node['y']

    def get_node_elevation(self, node):
        return self.__G.nodes[node]['elevation']
    
    def get_best_path(self, k):
        k_paths = self.get_k_shortest_paths(k)
        best_path_score = sys.maxsize
        best_elevation_change = 0
        best_path_dist = 0

        for path in k_paths:
            dist = 0
            elevation_change = 0

            for i in range(0, len(path) - 1):
                node1 = path[i]
                node2 = path[i + 1]

                # dist += ox.distance.euclidean_dist_vec(self.get_node_latitude(node1), self.get_node_longitiude(node1), self.get_node_latitude(node2), self.get_node_longitiude(node2))

                dist += self.__G.get_edge_data(node1,node2)['x']['length']

                elevation_change += abs(self.get_node_elevation(node1) - self.get_node_elevation(node2))

            if dist + elevation_change < best_path_score:
                best_path_score = dist + elevation_change
                best_elevation_change = elevation_change
                best_path_dist = dist
                best_path = path
                
        return best_path,best_elevation_change,best_path_dist