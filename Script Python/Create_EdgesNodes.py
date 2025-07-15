import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point

#Load file jalan format GeoJSON
gdf = gpd.read_file("/mnt/d/ProjectOSM/output/jalan.geojson")
print("Jumlah ruas jalan:", len(gdf))

#Membuat graf dari LineString
G = nx.Graph()
for idx, row in gdf.iterrows():
    if isinstance(row.geometry, LineString):
        coords = list(row.geometry.coords)
        for i in range(len(coords) - 1):
            u = coords[i]
            v = coords[i + 1]
            dist = Point(u).distance(Point(v))  # Jarak Euclidean
            G.add_edge(u, v, weight=dist, highway=row.get('highway'), name=row.get('name'))

#Membuat GeoDataFrame untuk EDGES
edge_data = []
for u, v, data in G.edges(data=True):
    edge_data.append({
        'from_x': u[0],
        'from_y': u[1],
        'to_x': v[0],
        'to_y': v[1],
        'weight': data.get('weight'),
        'highway': data.get('highway'),
        'name': data.get('name'),
        'geometry': LineString([u, v])
    })

edges = gpd.GeoDataFrame(edge_data, geometry='geometry')
print("Jumlah edges:", len(edges))

#Membuat GeoDataFrame untuk NODES
node_data = []
for node in G.nodes():
    node_data.append({
        'x': node[0],
        'y': node[1],
        'geometry': Point(node)
    })

nodes = gpd.GeoDataFrame(node_data, geometry='geometry')
print("Jumlah nodes:", len(nodes))

#Mendefinisikan CRS(jika belum ada)
edges.set_crs(epsg=4326, inplace=True)
nodes.set_crs(epsg=4326, inplace=True)

#Save ke CSV dan Geojson
edges.to_csv("/mnt/d/ProjectOSM/output/rekap_jalan_edges.csv", index=False)
nodes.to_csv("/mnt/d/ProjectOSM/output/rekap_jalan_nodes.csv", index=False)

edges.to_file("/mnt/d/ProjectOSM/output/jalan_edges.geojson", driver="GeoJSON")
nodes.to_file("/mnt/d/ProjectOSM/output/jalan_nodes.geojson", driver="GeoJSON")

