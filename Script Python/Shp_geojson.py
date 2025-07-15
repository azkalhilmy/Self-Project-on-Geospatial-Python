import geopandas as gpd

# Baca shapefile
shp_path = "/mnt/d/ProjectOSM/Raw/Kecamatan.shp"
gdf = gpd.read_file(shp_path)

# Simpan ke GeoJSON
geojson_path = "/mnt/d/ProjectOSM/Raw/Kecamatan.geojson"
gdf.to_file(geojson_path, driver="GeoJSON")

print("Konversi selesai! File tersimpan di:", geojson_path)
