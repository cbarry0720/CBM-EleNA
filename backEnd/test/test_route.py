import mock as mock
import pytest
from backEnd.elenaBackend import create_app
from backEnd.elenaBackend.get_path_between import get_path_between
import json
import networkx as nx
import osmnx as ox
from unittest import mock
@pytest.fixture()
def app():
    app = create_app()

    yield app
@pytest.fixture()
def client(app):
    return app.test_client()

def test_3NodeGraph():
    graph = nx.MultiDiGraph()
    graph.add_node(1,y=0, x=0,street_count= 4, elevation=64)
    graph.add_node(2, y=100, x=100, street_count=4, elevation=96)
    graph.add_node(3, y=100, x=100, street_count=4, elevation=32)
    graph.add_edge(1,2,weight=10,length=5)
    graph.add_edge(2,3,weight=10,length=1)
    graph.add_edge(1,3,weight=10,length=5)

    graph.graph["crs"] = "epsg:4326"
    pathBetween = get_path_between(1, 3, graph)
    pathBetween.set_start_node(1)
    pathBetween.set_end_node(3)
   # assert getPathBetween(graph,1,3,2)[2] == 0
    assert pathBetween.get_best_path(2)[1] == 32

def test_5NodeGraphSameLengths():
    graph = nx.MultiDiGraph()
    graph.add_node(1,y=0, x=0,street_count=4, elevation=64)
    graph.add_node(2, y=100, x=100, street_count=4, elevation=16)
    graph.add_node(3, y=100, x=100, street_count=4, elevation=32)
    graph.add_node(4, y=100, x=100, street_count=4, elevation=32)
    graph.add_node(5, y=100, x=100, street_count=4, elevation=64)
    graph.add_edge(1,2,weight=10,length=5)
    graph.add_edge(2,3,weight=10,length=5)
    graph.add_edge(3,5,weight=10,length=5)
    graph.add_edge(1,4,weight=10,length=5)
    graph.add_edge(4,5, weight=10, length=5)
    graph.graph["crs"] = "epsg:4326"
    pathBetween = get_path_between(1, 5, graph)
    pathBetween.set_start_node(1)
    pathBetween.set_end_node(5)
   # assert getPathBetween(graph,1,3,2)[2] == 0
    assert pathBetween.get_best_path(2)[1] == 64
    assert pathBetween.get_best_path(2)[2] == 10
def test_SameStartAndEnd(client):
    response = client.get('/route?start=spoke amherst&finish=spoke amherst&routeMultiplier=1')
    responseTxt = json.loads(response.data.decode('utf-8'))
    assert responseTxt["totalElevation"] == 0



def test_apiCallDeciphered(app,client, mocker):
    #Ensure calls to the api are being made entrusting api to work
    mockRequest = mocker.patch("osmnx.geocode")
    response = client.get('/route?start=spoke amherst&finish=stackers amherst&routeMultiplier=1')
    mockRequest.assert_any_call("spoke amherst")
    mockRequest.assert_any_call("stackers amherst")

def test_emptyStrings(client):
    response = client.get('/route?start=&finish=&routeMultiplier=')
    responseTxt = response.data.decode('utf-8')
    assert len(responseTxt) == 0
    assert responseTxt == ""

def test_SpokeStackersPath(client):
    response = client.get('/route?start=spoke amherst&finish=stackers amherst&routeMultiplier=1')
    responseTxt = json.loads(response.data.decode('utf-8'))
    assert responseTxt["totalElevation"] == 8

