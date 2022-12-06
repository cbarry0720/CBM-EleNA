import pandas as pd
import get_elevation
import networkx as nx
import numpy as np
import osmnx as ox
from requests import get
from pandas import json_normalize
ox.config(log_console=True, use_cache=True)


place = 'Amherst, MA'
G = ox.graph_from_place(place)

def elevation(a,b):
    a = G.nodes.get(a)
    b = G.nodes.get(b)
    x1 = a['x']
    y1 = a['y']
    x2 = b['x']
    y2 = b['y']
    a_elevation = get_elevation.get_elevation(y1,x1)
    b_elevation = get_elevation.get_elevation(y2,x2)

    return abs(a_elevation - b_elevation)

path = nx.astar_path(G, 8454349134, 2262120525, heuristic=elevation, weight="cost")


newGraph = nx.subgraph(G, path)
fig, ax = ox.plot_graph(newGraph, figsize=(17,17))