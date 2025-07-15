#Import semua lib yang dibutuhkan
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from shapely.geometry import box
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors

#Membaca data rumah sakit dan batas kecamatan
hospital_fp = "/mnt/d/ProjectOSM/output/hospital_centroid.geojson" 
hospitals = gpd.read_file(hospital_fp)

kecamatan_fp = "/mnt/d/ProjectOSM/Raw/kecamatan.geojson" 
kecamatan = gpd.read_file(kecamatan_fp)

#Memastikan CRS EPSG:4326 (WGS84)
if hospitals.crs != "EPSG:4326":
    hospitals = hospitals.to_crs(epsg=4326)
kecamatan = kecamatan.to_crs(epsg=4326)

#Mengambil koordinat rumah sakit
coords = [(geom.y, geom.x) for geom in hospitals.geometry]

#Membuat peta dasar
m = folium.Map(location=[lat, long], zoom_start=12, tiles='cartodbpositron')

#Heatmap Layer 
heatmap_fg = folium.FeatureGroup(name="Heatmap Rumah Sakit")
HeatMap(coords, radius=20, blur=10, max_zoom=13).add_to(heatmap_fg)
heatmap_fg.add_to(m)

#Marker Rumah Sakit
marker_fg = folium.FeatureGroup(name="Marker Rumah Sakit")
for idx, row in hospitals.iterrows():
    popup = row.get("name", "Rumah Sakit")
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=2,
        color="blue",
        fill=True,
        fill_opacity=0.5,
        popup=popup
    ).add_to(marker_fg)
marker_fg.add_to(m)

#Input Batas Kecamatan
kec_fg = folium.FeatureGroup(name="Batas Kecamatan")
folium.GeoJson(
    kecamatan,
    style_function=lambda x: {
        "color": "black",
        "weight": 1.5,
        "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(fields=["Nama_Kecamatan"], aliases=["Kecamatan:"])
).add_to(kec_fg)
kec_fg.add_to(m)

#Tambahkan label nama kecamatan ke peta
for _, row in kecamatan.iterrows():
    centroid = row.geometry.centroid
    nama_kec = row["Nama_Kecamatan"]
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f"""
            <div style="font-size:10pt; font-weight: bold; color: black; text-shadow: 1px 1px 2px white;">
                {nama_kec}
            </div>""")
    ).add_to(m)

#Fishnet Grid Jumlah RS
#Proyeksikan untuk fishnet
hospitals_proj = hospitals.to_crs(epsg=32749)
bounds = hospitals_proj.total_bounds

grid_size = 2000  # 2 km
xmin, ymin, xmax, ymax = bounds
rows = int(np.ceil((ymax - ymin) / grid_size))
cols = int(np.ceil((xmax - xmin) / grid_size))

grid_polygons = []
for i in range(cols):
    for j in range(rows):
        x0 = xmin + i * grid_size
        y0 = ymin + j * grid_size
        x1 = x0 + grid_size
        y1 = y0 + grid_size
        grid_polygons.append(box(x0, y0, x1, y1))

grid = gpd.GeoDataFrame(geometry=grid_polygons, crs="EPSG:32749")

#Hitung jumlah RS dalam grid
join = gpd.sjoin(hospitals_proj, grid, how="left", predicate="within")
counts = join.groupby("index_right").size()
grid["jumlah_rs"] = counts.reindex(grid.index).fillna(0)

#Proyeksikan kembali
grid_wgs = grid.to_crs(epsg=4326)

#Color scale
max_count = grid["jumlah_rs"].max()
colormap = cm.get_cmap('YlOrRd')
norm = colors.Normalize(vmin=0, vmax=max_count)

def get_color(value):
    rgba = colormap(norm(value))
    return colors.to_hex(rgba)

#Tambahkan grid ke peta
grid_fg = folium.FeatureGroup(name="Grid Jumlah RS per 2km²")
for _, row in grid_wgs.iterrows():
    jumlah = row["jumlah_rs"]
    color = get_color(jumlah)
    folium.GeoJson(
        row["geometry"],
        style_function=lambda x, color=color: {
            "fillColor": color,
            "color": "gray",
            "weight": 0.3,
            "fillOpacity": 0.6,
        },
        tooltip=folium.Tooltip(f"Jumlah RS: {int(jumlah)}")
    ).add_to(grid_fg)
grid_fg.add_to(m)

output_html = "/mnt/d/ProjectOSM/output/Peta-Heatmap.html"
m.save(output_html)
print(f" Peta Berhasil Dibuat: {output_html}")
