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
print(len(xValues))
for z in xValues:
    if len(xValues[z]) == 1:
        print(xValues[z])
        break
for key in G.nodes.keys():
    node = G.nodes.get(key)
    xval = node['x']
    yval = node['y']
    node['elevation'] = xValues[xval][yval]['elevation']
    print(node)


#for x in lists:
#    resultList.extend(x)
#print(len(resultList))
#print(len(G.nodes.values()))
#f = open("elevationTxt.txt", "w")
#f.write(json.dumps(resultList))

#f.close()

#print(requests.get(url[:-1]).text)
def getPathBetween(G,location1, location2,multiplier):
    nodeToMapToTup = ox.geocode(location1)
    nodeToMapFromTup = ox.geocode(location2)
    node1 = ox.nearest_nodes(G,nodeToMapFromTup[1],nodeToMapFromTup[0])
    node2 = ox.nearest_nodes(G,nodeToMapToTup[1],nodeToMapToTup[0])
    return nx.shortest_path(G,node1,node2)

app = Flask(__name__)
@app.route('/route')
def query_route():
    start = request.args.get('start')
    finish = request.args.get('finish')
    multiplier = request.args.get('routeMultiplier')
    pathBetween = getPathBetween(G,start,finish,multiplier)
    output = list()
    for x in pathBetween:
        output.append(G.nodes.get(x))
    result = outputObject(output,0,0)

    return result.toJSON()
class outputObject:
    def __init__(self,route,totalDistance,totalElevation):
        self.route = route
        self.totalDistance = totalDistance
        self.totalElevation = totalElevation
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
app.run(debug=True)