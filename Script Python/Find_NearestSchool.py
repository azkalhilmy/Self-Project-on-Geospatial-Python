import geopandas as gpd
import networkx as nx
import pandas as pd
from shapely.geometry import Point
from scipy.spatial import cKDTree
from tqdm import tqdm

#Mendefinisikan titik permukiman manual
permukiman_coords = [
    (110.417564, -6.949701), # Bandarharjo
    (110.436245, -6.944863), # Tj Mas
    (110.331582, -7.001044), # Ngaliyan
    (110.439481, -6.953242), # Semarang Timur
    (110.439649, -6.985510), # Semarang Timur 2
    (110.389140, -7.008549), # Gajahmungkur
    (110.444056, -7.009787), # Semarang Selatan
    (110.428590, -7.066967), # Banyumanik
    (110.442840, -7.071778), # Tembalang
    (110.424858, -7.006425), # Candisari
]

#Load jaringan jalan dan membangun graf
edges = gpd.read_file("/mnt/d/ProjectOSM/Raw/jalan_edges2.geojson")

G = nx.Graph()
for _, row in edges.iterrows():
    u = (row['from_x'], row['from_y'])
    v = (row['to_x'], row['to_y'])
    G.add_edge(u, v, weight=row['weight'])

print(f" Jumlah simpul: {len(G.nodes())}, ruas jalan: {len(G.edges())}")

#Load file sekolah (centroid)
sekolah = gpd.read_file("/mnt/d/ProjectOSM/Raw/sekolah_centroid.geojson")
sekolah_coords = list(sekolah.geometry.apply(lambda geom: (geom.x, geom.y)))
sekolah_names = list(sekolah['name'])

#Membuat KDTree dari sekolah
school_tree = cKDTree(sekolah_coords)

#Mencari sekolah terdekat berdasarkan jalan
def get_nearest_node(G, coord):
    return min(G.nodes(), key=lambda node: Point(node).distance(Point(coord)))

results = []

for idx, perm_coord in tqdm(enumerate(permukiman_coords), total=len(permukiman_coords)):
    start_node = get_nearest_node(G, perm_coord)

    # Cari 10 sekolah terdekat
    dists, idxs = school_tree.query(perm_coord, k=10)

    min_path_dist = float('inf')
    best_school_coord = None
    best_school_name = None

    for i in idxs:
        school_coord = sekolah_coords[i]
        school_name = sekolah_names[i]
        try:
            end_node = get_nearest_node(G, school_coord)
            dist = nx.shortest_path_length(G, source=start_node, target=end_node, weight='weight')
            if dist < min_path_dist:
                min_path_dist = dist
                best_school_coord = school_coord
                best_school_name = school_name
        except:
            continue

    results.append({
        "permukiman_coord": perm_coord,
        "sekolah_terdekat": best_school_coord,
        "nama_sekolah": best_school_name
    })

#Save ke CSV
df = pd.DataFrame(results)
df.to_csv("/mnt/d/ProjectOSM/output/Sekolah_terdekat.csv", index=False)
print("Data berhasil disimpan")

