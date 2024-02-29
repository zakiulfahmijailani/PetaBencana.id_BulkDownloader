import pandas as pd
import json
import geojson

def excel_to_geojson(excel_path):
    # Baca file Excel
    df = pd.read_excel(excel_path)
    
    # Ganti nilai NaN dengan nilai default
    df.fillna(0, inplace=True)  # Mengganti NaN dengan 0, sesuaikan sesuai kebutuhan
    
    # Buat fitur GeoJSON dari setiap baris
    features = []
    for _, row in df.iterrows():
        latitude, longitude = row['geometry_coordinates_1'], row['geometry_coordinates_0']
        if pd.notnull(latitude) and pd.notnull(longitude):
            point = geojson.Point((longitude, latitude))
            properties = row.to_dict()
            # Hapus kolom koordinat dari properties
            properties.pop('geometry_coordinates_0', None)
            properties.pop('geometry_coordinates_1', None)
            feature = geojson.Feature(geometry=point, properties=properties)
            features.append(feature)
    
    # Buat FeatureCollection
    feature_collection = geojson.FeatureCollection(features)
    
    # Simpan sebagai file GeoJSON
    with open('C:\\c.PetaBencana\\Data\\data_gabungan.geojson', 'w') as f:
        geojson.dump(feature_collection, f)

# Jalankan fungsi konversi
excel_path = 'C:\\c.PetaBencana\\Data\\data_gabungan.xlsx'
excel_to_geojson(excel_path)

print("Data berhasil disimpan sebagai GeoJSON.")
