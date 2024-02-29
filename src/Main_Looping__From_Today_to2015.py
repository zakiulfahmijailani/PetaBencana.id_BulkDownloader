'''
Jika Anda menjalankan kode ini, Anda akan mendapatkan seluruh data dari API PetaBencana mulai dari bulan ini hingga Januari 2015.
Kode ini secara otomatis mengatur rentang tanggal untuk setiap bulan, mengambil data laporan bencana dari API PetaBencana,
dan menyimpan data tersebut dalam bentuk file JSON.
Setiap file disimpan dalam direktori yang ditentukan dengan nama yang mencerminkan bulan dan tahun dari data yang diambil.
Proses ini berulang untuk setiap bulan, mulai dari bulan saat ini dan bergerak mundur hingga mencapai batas waktu Januari 2015.
'''

import requests
import json
import os
from datetime import datetime, timedelta

class PetaBencanaAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_reports(self, start_date, end_date, geoformat='geojson'):
        """Mengambil laporan dari API berdasarkan rentang tanggal dan format geo."""
        endpoint = f"{self.base_url}/reports/archive"
        params = {
            'start': start_date.strftime("%Y-%m-%dT%H:%M:%S+0700"),
            'end': end_date.strftime("%Y-%m-%dT%H:%M:%S+0700"),
            'geoformat': geoformat
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Gagal mendapatkan data dari API: {response.status_code}")

    def save_to_file(self, data, directory, filename):
        """Menyimpan data JSON ke dalam file."""
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data berhasil disimpan di {filepath}")

# Contoh penggunaan
if __name__ == "__main__":
    api = PetaBencanaAPI("https://api.petabencana.id")
    today = datetime.now()
    end_date = datetime(2015, 1, 1)  # Batas akhir adalah Januari 2015

    current_date = today
    while current_date >= end_date:
        # Atur start_date ke awal bulan saat ini
        start_of_month = current_date.replace(day=1)
        # Hitung end_date bulan ini dengan mencari tanggal awal bulan berikutnya, kemudian kurangi satu hari
        next_month = start_of_month + timedelta(days=32)
        start_of_next_month = next_month.replace(day=1)
        end_of_month = start_of_next_month - timedelta(days=1)
        
        try:
            data = api.get_reports(start_of_month, end_of_month)
            directory = "C:\\c.PetaBencana\\Data"
            filename = f"laporan_petabencana_{start_of_month.strftime('%Y-%m')}.json"
            api.save_to_file(data, directory, filename)
            print(f"Data untuk {start_of_month.strftime('%Y-%m')} berhasil disimpan.")
        except Exception as e:
            print(str(e))
        
        # Pindah ke bulan sebelumnya
        current_date = start_of_month - timedelta(days=1)
