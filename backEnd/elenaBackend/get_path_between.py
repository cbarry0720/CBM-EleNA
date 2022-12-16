import osmnx as ox
import sys
import json
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
        start_node = ox.nearest_nodes(self.__G, self.__start_loc[1], self.__start_loc[0])
        end_node = ox.nearest_nodes(self.__G, self.__end_loc[1], self.__end_loc[0])
        if self.__start_loc == self.__end_loc:
            return 0
        return ox.k_shortest_paths(self.__G, start_node,end_node, k)
    
    def get_node_longitiude(node):
        return node['x']

    def get_node_latitude(node):
        return node['y']

    def get_node_elevation(self, node):
        return self.__G.nodes[node]['elevation']

    def __get_path_between_adj_nodes(self, paths, node1, node2):
        best_path = None
        best_dist = sys.maxsize
        for path in paths:
            dist = self.__G.get_edge_data(node1,node2)[path]['length']
            if dist < best_dist:
                best_dist = dist
                best_path = path
        return best_path


    def get_best_path(self, k):
        paths = self.get_k_shortest_paths(k)
        if paths == 0:
            print("Start node is the same as end node")
            return None, None, None

        k_paths = list(paths)
        best_path_score = sys.maxsize
        best_elevation_change = 0
        best_path_dist = 0
        
        if len(k_paths) == 2:
            node1 = path[0]
            node2 = path[1]
            best_elevation_change =  abs(self.get_node_elevation(node1) - self.get_node_elevation(node2))
            best_path_dist =  self.__G.get_edge_data(node1,node2)[0]['length']
            best_path = k_paths
            return best_path,best_elevation_change,best_path_dist
        
        for path in k_paths:
            dist = 0
            elevation_change = 0

            for i in range(0, len(path) - 1):
                node1 = path[i]
                node2 = path[i + 1]
                
                smallest_between_two = self.__get_path_between_adj_nodes(self.__G.get_edge_data(node1,node2), node1, node2)
                dist += self.__G.get_edge_data(node1,node2)[smallest_between_two]['length']

                elevation_change += abs(self.get_node_elevation(node1) - self.get_node_elevation(node2))

            if dist + elevation_change < best_path_score:
                best_path_score = dist + elevation_change
                best_elevation_change = elevation_change
                best_path_dist = dist
                best_path = path
                
        return best_path,best_elevation_change,best_path_dist
