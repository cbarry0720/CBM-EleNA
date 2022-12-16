import osmnx as ox
import sys
import json
import math
class get_path_between:
    __start_loc = None
    __end_loc = None
    __G = None
    __start_node = None
    __end_node = None
    def __init__(self, start_loc, end_loc, G):
        self.__start_loc = ox.geocode(start_loc)
        self.__end_loc = ox.geocode(end_loc)
        self.__G = G
        self.__start_node = ox.nearest_nodes(self.__G, self.__start_loc[1], self.__start_loc[0])
        self.__end_node = ox.nearest_nodes(self.__G, self.__end_loc[1], self.__end_loc[0])

    #Used For Testing to bypass ox.nearestNodes
    def set_start_node(self,startNode):
        self.__start_node = startNode
    def set_end_node(self,endNode):
        self.__end_node = endNode;

    def get_k_shortest_paths(self, k):

        if self.__start_loc == self.__end_loc:
            return 0
        return ox.k_shortest_paths(self.__G, self.__start_node,self.__end_node, k)

    def get_node_elevation(self, node):
        if node == None:
            print('invalid node')
            return None
        return self.__G.nodes[node]['elevation']

    def __get_path_between_adj_nodes(self, paths, node1, node2):
        if node1 == None or node2 == None or paths == None:
            print('invalid input')
            return None

        best_path = None
        best_dist = sys.maxsize
        for path in paths:
            dist = self.__G.get_edge_data(node1,node2)[path]['length']
            if dist < best_dist:
                best_dist = dist
                best_path = path
        return best_path


    def minimize_total_dist(self, elevation_change, dist):
        return math.sqrt(elevation_change**2 + dist**2)

    def minimize_elevation_and_dist(self, elevation_change, dist):
        return elevation_change + dist

    def minimize_elevation(self, elevation_change, dist):
        return elevation_change
    def minimize_dist(self, elevation_change, dist):
        return dist

    def get_elevation_change(self, node1, node2):
        if node1 == None or node2 == None:
            print('invalid node')
            return None

        return abs(self.get_node_elevation(node1) - self.get_node_elevation(node2))

    def get_distance_change(self, node1, node2):
            if node1 == None or node2 == None:
                print('invalid node')
                return None
            smallest_between_two = self.__get_path_between_adj_nodes(self.__G.get_edge_data(node1,node2), node1, node2)
            return self.__G.get_edge_data(node1,node2)[smallest_between_two]['length']

    def get_best_path(self, k, minimizer):
        paths = self.get_k_shortest_paths(k)

        if paths == 0:
            print("Start node is the same as end node")
            return [self.__start_node], 0, 0

        k_paths = list(paths)
        best_path_score = sys.maxsize
        best_elevation_change = 0
        best_path_dist = 0

        for path in k_paths:
            dist = 0
            elevation_change = 0
            if len(path) == 2:
                node1 = path[0]
                node2 = path[1]
                elevation_change = abs(self.get_node_elevation(node1) - self.get_node_elevation(node2))
                dist = self.__G.get_edge_data(node1, node2)[0]['length']
            else:
                for i in range(0, len(path) - 1):
                    node1 = path[i]
                    node2 = path[i + 1]

                    smallest_between_two = self.__get_path_between_adj_nodes(self.__G.get_edge_data(node1,node2), node1, node2)
                    dist += self.__G.get_edge_data(node1,node2)[smallest_between_two]['length']

                    elevation_change += abs(self.get_node_elevation(node1) - self.get_node_elevation(node2))

            if dist + elevation_change < best_path_score:
                best_path_score = minimizer(elevation_change, dist)
                best_elevation_change = elevation_change
                best_path_dist = dist
                best_path = path
                
        return best_path,best_elevation_change,best_path_dist
