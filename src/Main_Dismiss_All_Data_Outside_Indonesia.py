import geojson
from shapely.geometry import shape, Point

# Batas geografis Indonesia
min_lat, max_lat = -11, 6
min_lon, max_lon = 95, 141

def filter_geojson(input_path, output_path):
    with open(input_path, 'r') as file:
        data = geojson.load(file)
    
    new_features = []
    for feature in data['features']:
        # Asumsikan bahwa koordinat berada dalam format [longitude, latitude]
        lon, lat = feature['geometry']['coordinates']
        if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
            new_features.append(feature)
    
    new_data = geojson.FeatureCollection(new_features)
    
    with open(output_path, 'w') as file:
        geojson.dump(new_data, file)

input_path = 'C:\c.PetaBencana\Data\data_gabungan.geojson'
output_path = 'C:\c.PetaBencana\Data\data_gabungan2.geojson'

filter_geojson(input_path, output_path)
