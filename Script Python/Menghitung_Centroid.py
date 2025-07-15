import geopandas as gpd
import pandas as pd 
from shapely.geometry import Point

#Load File POI
poi = gpd.read_file("/mnt/d/ProjectOSM/output/POI.geojson")

#Memproyeksikan ke CRS metrik *note: disesuaikan dengan zona UTM masing-masing
poi_projected = poi.to_crs(epsg=32749) #disini karena semarang UTM Zona 49s

#Memisahkan titik dan polygon
poi_point = poi_projected[poi_projected.geometry.type == 'Point']
poi_poly  = poi_projected[poi_projected.geometry.type.isin(['Polygon', 'MultiPolygon'])] 
#*note:Menggunakan Polygon dan MultiPolygon jika geometry Polygon disimpan dalam 2 tipe tersebut

#Mengambil centroid dari polygon
poi_poly_centroid = poi_poly.copy()
poi_poly_centroid['geometry'] = poi_poly_centroid.geometry.centroid

#Semua digabungin
poi_all_points_proj = pd.concat([poi_point, poi_poly_centroid], ignore_index=True)
poi_all_points = gpd.GeoDataFrame(poi_all_points_proj)
poi_all_points = poi_all_points.set_crs("EPSG:32749", allow_override=True)

#Balikin lagi ke Geografis WGS84 (EPSG:4326)
poi_all_points = poi_all_points.to_crs(epsg=4326)

#Simpan File
poi_all_points.to_file("/mnt/d/ProjectOSM/output/sekolah_centroid.geojson", driver="GeoJSON")
print("File POI sekolah berhasil digabungkan dan disimpan.")