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
from flask_cors import CORS, cross_origin
ox.config(log_console=True, use_cache=True)

place = 'Amherst, MA'
G = ox.graph_from_place(place)
#G = ox.add_node_elevations_raster(G,"C:/Users/Bryan McCaffery/Downloads/zipfolder/Elevation_Model.tif")
#nc = ox.plot.get_node_colors_by_attr(G, "elevation", cmap="plasma")
#fig, ax = ox.plot_graph(G, node_color=nc, node_size=5, edge_color="#333333", bgcolor="k")
#elevations = requests.get("https://api.open-elevation.com/api/v1/lookup?locations=10,10|20,20|41.161758,-8.583933")
#url = "https://api.open-elevation.com/api/v1/lookup?locations="
#i = 0
#totalResults = list()
#for x in G.nodes.values():
#    url = url + str(x['y']) + ","+str(x['x']) + "|"
#    i +=1
#    if i % 100 == 0:
#        curResults = requests.get(url[:-1]).json()["results"]
#        totalResults.append(curResults)

#        url = "https://api.open-elevation.com/api/v1/lookup?locations="
#        time.sleep(1)
#if url != "https://api.open-elevation.com/api/v1/lookup?locations=":
#    curResults = requests.get(url[:-1]).json()["results"]
#    totalResults.append(curResults)
#f = open("elevationTxt.txt", "w")
#f.write(json.dumps(totalResults))
#f.close()
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



#for x in lists:
#    resultList.extend(x)
#print(len(resultList))
#print(len(G.nodes.values()))
#f = open("elevationTxt.txt", "w")
#f.write(json.dumps(resultList))

#f.close()

#print(requests.get(url[:-1]).text)
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
    # for every path returned calculate the distance and total elevation change then return shortest path with smallest changes
    for path in K_paths:
        dist = 0
        elevation_change = 0

        for i in range(0, len(path) - 1):
            node1 = path[i]
            node2 = path[i + 1]
            # Get lat and long of nodes
            y1 = G.nodes[node1]['y']
            x1 = G.nodes[node1]['x']

            y2 = G.nodes[node2]['y']
            x2 = G.nodes[node2]['x']

            dist += ox.distance.euclidean_dist_vec(y1, x1, y2, x2)

            a_elevation = G.nodes[node1]['elevation']
            b_elevation = G.nodes[node2]['elevation']

            elevation_change += abs(a_elevation - b_elevation)

        if dist + elevation_change < best_val:
            best_val = dist + elevation_change
            best_elevation = elevation_change
            best_dist = dist
            best_path = path
    return best_path,best_elevation,best_dist

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/route')
@cross_origin()
def query_route():
    start = request.args.get('start')
    finish = request.args.get('finish')
    multiplier = int(request.args.get('routeMultiplier'))
    pathBetween = getPathBetween(G,start,finish,multiplier)
    output = list()
    for x in pathBetween[0]:
        output.append(G.nodes.get(x))
    result = outputObject(output,pathBetween[2],pathBetween[1])
    return result.toJSON()
class outputObject:
    def __init__(self,route,totalDistance,totalElevation):
        self.route = route
        self.totalDistance = totalDistance
        self.totalElevation = totalElevation
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
app.run(debug=True)