import pytest
from backEnd.elenaBackend import create_app
from backEnd.elenaBackend.get_path_between import get_path_between
import json
import networkx as nx

@pytest.fixture()
def app():
    app = create_app()

    yield app
@pytest.fixture()
def client(app):
    return app.test_client()

def test_SameStartAndEnd(client):
    response = client.get('/route?start=spoke amherst&finish=spoke amherst&routeMultiplier=1&min=True')
    responseTxt = json.loads(response.data.decode('utf-8'))
    assert responseTxt["totalElevation"] == 0



def test_apiCallDeciphered(app,client, mocker):
    #Ensure calls to the api are being made entrusting api to work
    mockRequest = mocker.patch("osmnx.geocode")
    response = client.get('/route?start=spoke amherst&finish=stackers amherst&routeMultiplier=1&min=True')
    mockRequest.assert_any_call("spoke amherst")
    mockRequest.assert_any_call("stackers amherst")

def test_emptyStrings(client):
    response = client.get('/route?start=&finish=&routeMultiplier=')
    responseTxt = response.data.decode('utf-8')
    assert len(responseTxt) == 0
    assert responseTxt == ""

def test_SpokeStackersPath(client):
    response = client.get('/route?start=spoke amherst&finish=stackers amherst&routeMultiplier=1&min=True')
    responseTxt = json.loads(response.data.decode('utf-8'))
    assert responseTxt["totalElevation"] == 8