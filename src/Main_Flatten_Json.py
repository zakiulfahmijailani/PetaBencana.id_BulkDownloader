import pandas as pd
import json

# Fungsi untuk meratakan JSON
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Lokasi file JSON
file_path = 'C:\c.PetaBencana\Data\laporan_petabencana_2019-09.json'

# Membaca file JSON
with open(file_path, 'r') as file:
    json_data = json.load(file)
    # Fokus pada data di dalam "features"
    features_data = json_data['result']['features']

# Meratakan setiap item dalam features dan mengumpulkan dalam list
flattened_data_list = [flatten_json(feature) for feature in features_data]

# Membuat DataFrame dari data yang telah diratakan
df = pd.DataFrame(flattened_data_list)

# Menyimpan DataFrame ke file Excel
output_excel_path = 'C:\c.PetaBencana\Data\laporan_petabencana_2019-09_flattened.xlsx'
df.to_excel(output_excel_path, index=False)

print("DataFrame telah disimpan ke Excel.")
