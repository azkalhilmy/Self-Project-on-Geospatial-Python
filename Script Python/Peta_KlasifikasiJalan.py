import folium
import geopandas as gpd
from branca.colormap import linear
import matplotlib.cm as cm
import matplotlib.colors as mcolors

#Load File jalan format GeoJSON
gdf = gpd.read_file("/mnt/d/ProjectOSM/output/jalan_edges2.geojson")

#Memastikan CRS nya EPSG:4326
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
    
#Memfilter hanya beberapa jenis jalan yang ingin ditampilkan
important_highways = [
    'motorway', 'pedestrian', 'residential', 'cycleway', 'track',
    'service', 'services', 'primary', 'secondary', 'trunk',
    'tertiary', 'unclassified'
]   #Ini bisa dilihat saat visualisasi di QGIS ataupun cek atribut tabel via python
gdf = gdf[gdf['highway'].isin(important_highways)]

#Mengambil tipe jalan setelah filtering
highway_types = gdf['highway'].dropna().unique()
highway_types.sort()

#Membuat color map
turbo = cm.get_cmap("turbo", len(highway_types))
color_map = {
    hwy: mcolors.to_hex(turbo(i / len(highway_types)))
    for i, hwy in enumerate(highway_types)
}

#Membuat peta folium
m = folium.Map(location=[isi latnya, isi longnya], zoom_start=12, tiles='cartodbpositron')

#Menambahkan GeoJSON untuk tiap tipe highway
for hwy in highway_types:
    sub_gdf = gdf[gdf['highway'] == hwy]
    folium.GeoJson(
        sub_gdf,
        name=f"{hwy}",
        style_function=lambda feature, color=color_map[hwy]: {
            'color': color,
            'weight': 2,
        },
#        tooltip=folium.GeoJsonTooltip(fields=['highway'], aliases=['Type']) #bisa diaktifkan jika dibutuhkan
    ).add_to(m)
 
#Tambahkan layer control
folium.LayerControl().add_to(m)

#Tambahkan legenda
legend_html = """
<div style="
    position: fixed; 
    bottom: 80px; left: 10px; width: 220px; height: auto; 
    z-index:9999; font-size:14px;
    background-color: white; padding: 10px; border:2px solid grey;
">
<b>Highway Type Legend</b><br>
"""
for hwy, color in color_map.items():
    legend_html += f'<i style="background:{color};width:12px;height:12px;display:inline-block;margin-right:5px;"></i>{hwy}<br>'
legend_html += "</div>"
m.get_root().html.add_child(folium.Element(legend_html))

#Tambahkan watermark
watermark_html = """
<div style="
    position: fixed;
    bottom: 10px;
    right: 10px;
    z-index: 9999;
    font-size: 15px;
    color: green;
    background: rgba(255,255,255,0.5);
    padding: 3px 8px;
    border-radius: 5px;
    font-family: Arial, sans-serif;
">
    © Hilmy Azkal Adzkiya
</div>
"""
m.get_root().html.add_child(folium.Element(watermark_html))

# Save map
m.save("/mnt/d/ProjectOSM/output/PetaJalan_KotaSemarang.html")
