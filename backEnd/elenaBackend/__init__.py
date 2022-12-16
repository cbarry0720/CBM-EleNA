import osmnx as ox
import json
import json
from flask import Flask, request, jsonify
import logging
from backEnd.elenaBackend.get_path_between import get_path_between
from flask_cors import CORS, cross_origin


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
    CORS(app)
    G = iniateGraph()
    # a simple page that says hello


    @app.route('/route')
    @cross_origin()
    def query_route():
        start = request.args.get('start')
        finish = request.args.get('finish')
        min = request.args.get('min')

        if start is None or finish is None or start == "" or finish == "":
            app.logger.warning("Either empty strings or missing parameters")
            return ""
        multiplier = int(request.args.get('routeMultiplier'))
        app.logger.info("Request Received for route between " + start + " and " + finish + " with multiplier " + str(multiplier))
        pathBetween = get_path_between(start, finish, G)
        bestPathBetween = pathBetween.get_best_path(multiplier,pathBetween.minimize_elevation_and_dist, min)
        output = list()
        for nodes in bestPathBetween[0]:
            output.append(G.nodes.get(nodes))
        result = outputObject(output, bestPathBetween[2], bestPathBetween[1])
        return result.toJSON()

    return app


class outputObject:
    def __init__(self,route,totalDistance,totalElevation):
        self.route = route
        self.totalDistance = totalDistance
        self.totalElevation = totalElevation
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

