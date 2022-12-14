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

def test_3NodeGraph_max():
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


def test_input_validation():
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
    assert pathBetween.get_elevation_change(1, None) == None
    assert pathBetween.get_elevation_change(None, 1) == None

    assert pathBetween.get_path_between_adj_nodes(None, 1,2) == None
    assert pathBetween.get_path_between_adj_nodes(1, None,2) == None
    assert pathBetween.get_path_between_adj_nodes(1, 2,None) == None
    assert pathBetween.get_node_elevation(None) == None

    
    pathBetween = get_path_between(1, 1, graph)
    pathBetween.set_start_node(1)
    pathBetween.set_end_node(1)
    assert pathBetween.get_k_shortest_paths(1) == 0
    assert pathBetween.get_best_path(2,pathBetween.minimize_elevation_and_dist,True)[0] == [1]

def test_3NodeGraph_min_dist():
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
    assert pathBetween.get_best_path(1,pathBetween.minimize_dist,True)[1] == 32

def test_3NodeGraph_max_dist():
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
    assert pathBetween.get_best_path(1,pathBetween.minimize_dist,False)[1] == 32

def test_3NodeGraph_min_elevation():
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
    assert pathBetween.get_best_path(1,pathBetween.minimize_elevation,True)[2] == 5

def test_3NodeGraph_max_elevation():
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
    assert pathBetween.get_best_path(1,pathBetween.minimize_elevation,False)[2] == 5

def test_3NodeGraph_min_totalDist():
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
    assert pathBetween.get_best_path(1,pathBetween.minimize_total_dist,True)[1] == 32
