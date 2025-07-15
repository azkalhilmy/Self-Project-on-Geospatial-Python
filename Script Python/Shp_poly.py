import geopandas as gpd

def write_osmium_poly(gdf, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{filename}\n")
        for idx, geom in enumerate(gdf.geometry):
            if geom.geom_type == 'Polygon':
                f.write("1\n")
                for x, y in geom.exterior.coords:
                    f.write(f" {x} {y}\n")
                f.write("END\n")
            elif geom.geom_type == 'MultiPolygon':
                for part in geom.geoms:
                    f.write("1\n")
                    for x, y in part.exterior.coords:
                        f.write(f" {x} {y}\n")
                    f.write("END\n")
        f.write("END\n")

#Path input/output
input_shp = "/mnt/d/ProjectOSM/Raw/Semarang.shp"
output_poly = "/mnt/d/ProjectOSM/working/Semarang.poly"

#Load dan cek projection
gdf = gpd.read_file(input_shp)
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")

write_osmium_poly(gdf, output_poly)
print(f"File berhasil disimpan")
