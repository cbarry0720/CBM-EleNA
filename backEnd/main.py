import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString, Polygon
import networkx as nx
import osmnx as ox
import json
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from IPython.display import IFrame
import json
from flask import Flask, request, jsonify
ox.config(log_console=True, use_cache=True)

place = 'Amherst, MA'
G = ox.graph_from_place(place)


def getPathBetween(G,location1, location2):
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
    pathBetween = getPathBetween(G,start,finish)
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