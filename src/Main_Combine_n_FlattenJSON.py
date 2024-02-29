import pandas as pd
import json
import os

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

directory = "C:\\c.PetaBencana\\Data"
combined_df = pd.DataFrame()

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Fokus pada data di dalam "features" jika struktur JSON-nya sesuai
            if 'result' in data and 'features' in data['result']:
                features_data = data['result']['features']
                flattened_data_list = [flatten_json(feature) for feature in features_data]
                temp_df = pd.DataFrame(flattened_data_list)
            else:
                flattened_data = flatten_json(data)
                temp_df = pd.DataFrame([flattened_data])
            combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

# Sesuaikan path sesuai kebutuhan
output_excel_path = "C:\\c.PetaBencana\\Data\\data_gabungan.xlsx"
combined_df.to_excel(output_excel_path, index=False)

print("Data berhasil disimpan sebagai Excel.")
