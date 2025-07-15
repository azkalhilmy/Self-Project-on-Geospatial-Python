import geopandas as gpd
import networkx as nx
import pandas as pd
from shapely.geometry import Point
from pyproj import Transformer
import folium
from tqdm import tqdm
from branca.element import Template, MacroElement

#Input Koordinat permukiman dan Rumah Sakit
permukiman_coords = [
    (110.417564, -6.949701),  # bandarharjo
    (110.436245, -6.944863),  # tjmas
    (110.331582, -7.001044),  # ngaliyan
    (110.439481, -6.953242),  # smgtimur
    (110.439649, -6.985510),  # smgtimur2
    (110.389140, -7.008549),  # gjmungkur
    (110.444056, -7.009787),  # smgsel
    (110.428590, -7.066967),  # bymanik
    (110.442840, -7.071778),  # tembalang
    (110.424858, -7.006425),  # candisari
]

rs_coord = (110.407287, -6.994579)  # Koordinat Rumah Sakit

#Load jaringan jalan dan proyeksikan ke metrik
edges = gpd.read_file("/mnt/d/ProjectOSM/Raw/jalan_edges.geojson")
edges = edges.to_crs(epsg=32749)  # Proyeksi ke meter

#Buat graf dari hasil proyeksi
G = nx.Graph()
for _, row in edges.iterrows():
    if row.geometry and row.geometry.geom_type == 'LineString':
        coords = list(row.geometry.coords)
        for i in range(len(coords) - 1):
            u = coords[i]
            v = coords[i + 1]
            dist = Point(u).distance(Point(v))
            G.add_edge(u, v, weight=dist)

#Transformasi sistem proyeksi koordinat permukiman & RS ke UTM
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32749", always_xy=True)
permukiman_proj = [transformer.transform(lon, lat) for lon, lat in permukiman_coords]
rs_coord_proj = transformer.transform(rs_coord[0], rs_coord[1])

#Mencari simpul terdekat
def get_nearest_node(G, coord):
    return min(G.nodes(), key=lambda node: Point(node).distance(Point(coord)))

#Mencari shortest path
results = []
paths_all = []

print(" Proses menghitung shortest path permukiman → RS... yang sabar hehe ")
for i, perm in enumerate(tqdm(permukiman_proj)):
    start_node = get_nearest_node(G, perm)
    end_node   = get_nearest_node(G, rs_coord_proj)

    try:
        path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
        dist_m = nx.path_weight(G, path, weight='weight')
        waktu_menit = round(dist_m / 1.39 / 60, 2)  # Pendekatan Rata-Rata Jalan kaki 5 km/jam

        results.append({
            "id": i+1,
            "permukiman_lon": permukiman_coords[i][0],
            "permukiman_lat": permukiman_coords[i][1],
            "rs_lon": rs_coord[0],
            "rs_lat": rs_coord[1],
            "jarak_km": round(dist_m / 1000, 2),
            "estimasi_waktu_menit": waktu_menit
        })

        paths_all.append(path)

    except Exception as e:
        print(f"Gagal permukiman {i+1}: {e}")

#Simpan ke CSV
df = pd.DataFrame(results)
output_csv = "/mnt/d/ProjectOSM/output/Permukiman_Ke_RS.csv"
df.to_csv(output_csv, index=False)
print(f"Yuhuu, Hasil sudah disimpan: {output_csv}")

#Membuat Peta di Folium
m = folium.Map(location=[lat, long], zoom_start=12, tiles="cartodbpositron")

#Tambahkan jalur
for idx, path in enumerate(paths_all):
    coords = [(y, x) for x, y in path]  # dari (lon, lat) ke (lat, lon)
    folium.PolyLine(
        coords,
        color="(sesuai selera)",
        weight= 3,
        opacity= (sesuaikan),
        tooltip=f"Rute {idx+1}"
    ).add_to(m)

#Tambahkan point marker permukiman
for idx, (lon, lat) in enumerate(permukiman_coords):
    folium.Marker(
        location=[lat, lon],
        popup=f"Permukiman {idx+1}",
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(m)

#Tambahkan point marker rumah sakit
folium.Marker(
    location=[rs_coord[1], rs_coord[0]],
    popup="Rumah Sakit",
    icon=folium.Icon(color="green", icon="plus-sign")
).add_to(m)

#Tambahkan legenda
legend_html = """
{% macro html(this, kwargs) %}
<div style="position: fixed; bottom: 50px; left: 50px; width: 200px; background-color: white; border:2px solid grey; border-radius:5px; padding: 10px; font-size:14px; z-index:9999;">
<b>Legenda:</b><br>
<i style="color:red;">&#9632;</i> Jalur tercepat<br>
<i style="color:blue;">&#9679;</i> Titik Permukiman<br>
<i style="color:green;">&#9679;</i> Rumah Sakit
</div>
{% endmacro %}
"""
legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().add_child(legend)

#Simpan file
m.save("/mnt/d/ProjectOSM/output/Aksesibilitas_RS.html")
print("Peta berhasil dibuat")
