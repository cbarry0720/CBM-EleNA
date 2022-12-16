import os

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import Point, LineString, Polygon
import networkx as nx
import osmnx as ox
import json
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from IPython.display import IFrame
import rasterio
import json
from flask import Flask, request, jsonify
import time
import logging


place = 'Amherst, MA'
G = ox.graph_from_place(place)
f = open("elevationTxt.txt","r")
resultList = list()
lists = json.load(f)
#print(lists)
f.close()
xValues = dict()
for x in lists:
    if xValues.get(x['longitude']) is None:
        xValues[x['longitude']] = {x['latitude']:x}
    else:
        xValues[x['longitude']][x['latitude']] = x


for key in G.nodes.keys():
    node = G.nodes.get(key)
    xval = node['x']
    yval = node['y']
    node['elevation'] = xValues[xval][yval]['elevation']
    if node['elevation'] is None:
        print("Error")


def create_app(test_config=None):
    # create and configure the app
    logging.basicConfig(filename='record.log', level=logging.DEBUG)
    app = Flask(__name__, instance_relative_config=True)
    # a simple page that says hello

    @app.route('/route')
    def query_route():
        start = request.args.get('start')
        finish = request.args.get('finish')
        if start is None or finish is None or start == "" or finish == "":
            app.logger.warning("Either empty strings or missing parameters")
            return ""
        multiplier = int(request.args.get('routeMultiplier'))
        app.logger.info("Request Received for route between " + start + " and " + finish + " with multiplier " + str(multiplier))
        pathBetween = getPathBetween(G, start, finish, multiplier)
        output = list()
        for x in pathBetween[0]:
            output.append(G.nodes.get(x))
        result = outputObject(output, pathBetween[2], pathBetween[1])
        return result.toJSON()

    @app.route('/graph')
    def getGraph():
        print(G.graph["crs"])
        for x in G.nodes:
            print(x)
            print(G.nodes.get(x))
            return x

    return app

class outputObject:
    def __init__(self,route,totalDistance,totalElevation):
        self.route = route
        self.totalDistance = totalDistance
        self.totalElevation = totalElevation
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

def getPathBetween(G,start, end,k=2):
    # get the gecode location for the start and end location
    start_loc = ox.geocode(start)
    end_loc = ox.geocode(end)
    # get the nearest node in the grapgh of amherst to the ask locations
    start_node = ox.nearest_nodes(G, start_loc[1], start_loc[0])
    end_node = ox.nearest_nodes(G, end_loc[1], end_loc[0])

    # get the k shortest paths from start location to end location
    paths = ox.k_shortest_paths(G, start_node, end_node, k)

    K_paths = list(paths)
    best_path = []
    best_val = 99999999999
    best_elevation = 0
    best_dist = 0
    print(len(K_paths))
    # for every path returned calculate the distance and total elevation change then return shortest path with smallest changes
    for path in K_paths:
        dist = 0
        elevation_change = 0
        print("Hmmm")
        for i in range(0, len(path) - 1):
            print("Hmmm")
            node1 = path[i]
            node2 = path[i + 1]
            # Get lat and long of nodes
            y1 = G.nodes[node1]['y']
            x1 = G.nodes[node1]['x']

            y2 = G.nodes[node2]['y']
            x2 = G.nodes[node2]['x']
            for x in G.get_edge_data(node1,node2):
                print(G.get_edge_data(node1,node2)[x]['length'])
            dist += ox.distance.euclidean_dist_vec(y1, x1, y2, x2)
            print(dist)
            a_elevation = G.nodes[node1]['elevation']
            b_elevation = G.nodes[node2]['elevation']

            elevation_change += abs(a_elevation - b_elevation)

        if dist + elevation_change < best_val:
            best_val = dist + elevation_change
            best_elevation = elevation_change

            best_dist = dist

            best_path = path


    return best_path,best_elevation,best_dist