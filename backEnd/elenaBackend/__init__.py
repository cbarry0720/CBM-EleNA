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
from backEnd.elenaBackend.get_path_between import get_path_between


def iniateGraph():
    place = 'Amherst, MA'
    graph = ox.graph_from_place(place)
    f = open("elevationTxt.txt", "r")
    resultList = list()
    lists = json.load(f)
    # print(lists)
    f.close()
    xValues = dict()
    for x in lists:
        if xValues.get(x['longitude']) is None:
            xValues[x['longitude']] = {x['latitude']: x}
        else:
            xValues[x['longitude']][x['latitude']] = x

    for key in graph.nodes.keys():
        node = graph.nodes.get(key)
        xval = node['x']
        yval = node['y']
        node['elevation'] = xValues[xval][yval]['elevation']
    return graph


def create_app(test_config=None):
    # create and configure the app
    logging.basicConfig(filename='record.log', level=logging.DEBUG)
    app = Flask(__name__, instance_relative_config=True)
    G = iniateGraph()
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
        pathBetween = get_path_between(start, finish, G).get_best_path(multiplier)
        output = list()
        for nodes in pathBetween[0]:
            output.append(G.nodes.get(nodes))
        result = outputObject(output, pathBetween[2], pathBetween[1])
        return result.toJSON()

    return app


class outputObject:
    def __init__(self,route,totalDistance,totalElevation):
        self.route = route
        self.totalDistance = totalDistance
        self.totalElevation = totalElevation
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

