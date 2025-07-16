import geopandas as gpd
import networkx as nx
from shapely.geometry import Point

#Load edges format geojson
edges = gpd.read_file("/mnt/d/ProjectOSM/Raw/jalan_edges2.geojson")

#Bangun graf dari edges
G = nx.Graph()
for _, row in edges.iterrows():
    u = (row['from_x'], row['from_y'])
    v = (row['to_x'], row['to_y'])
    G.add_edge(u, v, weight=row['weight'], highway=row.get('highway'), name=row.get('name'))

#Analisis Betweenness Centrality
print("Proses menghitung approx betweenness centrality dengan k=100")
bet_centrality = nx.betweenness_centrality(G, k=100, weight='weight', normalized=True, seed=42)

#Buat GeoDataFrame simpul dengan nilai betweenness
node_geoms = []
node_bet = []
for node, val in bet_centrality.items():
    node_geoms.append(Point(node))
    node_bet.append(val)

gdf_nodes = gpd.GeoDataFrame({'betweenness': node_bet}, geometry=node_geoms, crs="EPSG:4326")
gdf_nodes.to_file("/mnt/d/ProjectOSM/analisis/betweennessappr.geojson", driver="GeoJSON")
print("Hasil betweenness centrality sudah tersimpan")
