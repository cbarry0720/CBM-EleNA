import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString, Polygon
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from IPython.display import IFrame

# this code is an example of plotting a path from pufton to the education buidling 

ox.config(log_console=True, use_cache=True)
def dist(a,b):
    print(a)
    a = G.nodes.get(a)
    b = G.nodes.get(b)
    x1 = a['x']
    y1 = a['y']
    x2 = b['x']
    y2 = b['y']
    return ((x1 - x2) ** 2 + (y1 - y2)  ** 2) ** 0.5
place = 'Amherst, MA'
G = ox.graph_from_place(place)

path = nx.astar_path(G, 8454349134, 2262120525, heuristic=dist, weight="cost")


newGraph = nx.subgraph(G, path)
fig, ax = ox.plot_graph(newGraph, figsize=(17,17))