import pytest
from backEnd.elenaBackend.get_path_between import get_path_between
import networkx as nx


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
    assert pathBetween.get_best_path(2,pathBetween.minimize_elevation_and_dist,True)[1] == 32

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
    assert pathBetween.get_best_path(2,pathBetween.minimize_elevation_and_dist,False)[1] == 96

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
    assert pathBetween.get_best_path(2,pathBetween.minimize_elevation_and_dist,True)[1] == 64
    assert pathBetween.get_best_path(2,pathBetween.minimize_elevation_and_dist,True)[2] == 10

def test_3NodeGraphTotalDistance():
    graph = nx.MultiDiGraph()
    graph.add_node(1,y=0, x=0,street_count=4, elevation=2)
    graph.add_node(2, y=100, x=100, street_count=4, elevation=2)
    graph.add_node(3, y=100, x=100, street_count=4, elevation=4)
    graph.add_edge(1,2,weight=10,length=2)
    graph.add_edge(2,3,weight=10,length=2)

    graph.graph["crs"] = "epsg:4326"
    pathBetween = get_path_between(1, 3, graph)
    pathBetween.set_start_node(1)
    pathBetween.set_end_node(3)
   # assert getPathBetween(graph,1,3,2)[2] == 0
    assert pathBetween.get_best_path(2,pathBetween.minimize_total_dist,True)[2] == 4
    assert pathBetween.get_best_path(2,pathBetween.minimize_elevation_and_dist,True)[1] == 2


