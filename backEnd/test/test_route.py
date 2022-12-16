import mock as mock
import pytest
from backEnd.elenaBackend import create_app,getPathBetween
import json
import networkx as nx
import osmnx as ox
from unittest import mock
@pytest.fixture()
def app():
    app = create_app()

    yield app


def test_buildGraph():
    graph = nx.MultiDiGraph()
    graph.add_node(1,y=0, x=0,street_count= 4, elevation=64)
    graph.add_node(2, y=100, x=100, street_count=4, elevation=64)
    graph.add_node(3, y=100, x=100, street_count=4, elevation=64)
    graph.add_edge(1,2,weight=10,length=5)
    graph.add_edge(2,3,weight=10,length=10)
    graph.add_edge(1,3,weight=25,length=100)

    graph.graph["crs"] = "epsg:4326"

   # assert getPathBetween(graph,1,3,2)[2] == 0
    assert getPathBetween(graph, 1, 3)[1] == 0


@pytest.fixture()
def client(app):
    return app.test_client()

def test_apiCallDeciphered(app,client, mocker):
    #Ensure calls to the api are being made entrusting api to work
    mockRequest = mocker.patch("osmnx.geocode")
    response = client.get('/route?start=spoke amherst&finish=stackers amherst&routeMultiplier=1')
    mockRequest.assert_any_call("spoke amherst")
    mockRequest.assert_any_call("stackers amherst")

def test_emptyStrings(client):
    response = client.get('/route?start=&finish=&routeMultiplier=')
    print(response.data.decode('utf-8'))
    responseTxt = response.data.decode('utf-8')
    assert len(responseTxt) == 0
    assert responseTxt == ""

def test_SpokeStackersPath(client):
    response = client.get('/route?start=spoke amherst&finish=stackers amherst&routeMultiplier=1')
    print(response.data.decode('utf-8'))
    responseTxt = json.loads(response.data.decode('utf-8'))
    assert responseTxt["totalElevation"] == 8

