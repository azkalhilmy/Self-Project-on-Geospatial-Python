import geopandas as gpd

#Load File POI
gdf_fasilitas = gpd.read_file("/mnt/d/ProjectOSM/output/POI_Semarang.geojson")

#Load File Batas Kelurahan Format geojson
gdf_admin = gpd.read_file("/mnt/d/ProjectOSM/Raw/BatasKelurahan.geojson")
gdf_admin = gdf_admin.rename(columns={'NAMOBJ': 'kelurahan'}) #Karena kolom kelurahan pada kolom 'NAMOBJ'

print(gdf_fasilitas.crs)
print(gdf_admin.crs)

#Melakukan Join Spasial untuk mencari fasilitas (POI) yang berada dalam kelurahan
gdf_joined = gpd.sjoin(gdf_fasilitas, gdf_admin, how='inner', predicate='within')

#Menghitung jumlah fasilitas per kelurahan per jenis
rekap = gdf_joined.groupby(['kelurahan', 'amenity']).size().unstack(fill_value=0)

#Merge ke semua kelurahan agar yang nol tetap muncul
all_kel = gdf_admin[['kelurahan']].drop_duplicates()
rekap_full = all_kel.merge(rekap, how='left', on='kelurahan').fillna(0).set_index('kelurahan')
rekap_full.to_csv("/mnt/d/ProjectOSM/output/RekapPOI_Kelurahan.csv")

# Tampilkan hasil
print(rekap_full.to_string())


