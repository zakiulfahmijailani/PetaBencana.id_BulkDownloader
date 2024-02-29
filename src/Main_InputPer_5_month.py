'''
Jika Anda menjalankan program ini, Anda akan diminta untuk memasukkan tahun, bulan, dan tanggal dari mana Anda ingin
mulai mencari data di api.petabencana.id dan sampai tahun, bulan, dan tanggal mana pencarian harus berakhir, dihitung mundur
5 bulan ke belakang dari tanggal mulai. Ingat, data dalam API ini hanya tersedia sampai Desember 2016 saja.
Setelah memasukkan rentang tanggal tersebut, program akan mengambil laporan bencana dari API PetaBencana sesuai dengan rentang
tanggal yang diberikan dan menyimpannya dalam format JSON ke dalam direktori yang telah ditentukan di sistem file Anda.
File tersebut akan dinamai "laporan_petabencana.json". Melalui proses ini, pengguna dapat mengakses dan menyimpan data historis
bencana secara sistematis untuk analisis lebih lanjut atau keperluan dokumentasi.
'''

import requests
import json
import os

class PetaBencanaAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def format_date(self, year, month, day):
        """Mengubah format tanggal menjadi format yang diinginkan oleh API."""
        return f"{year}-{month}-{day}T00:00:00+0700"

    def get_reports(self, start_date, end_date, geoformat='geojson'):
        """Mengambil laporan dari API berdasarkan rentang tanggal dan format geo."""
        endpoint = f"{self.base_url}/reports/archive"
        params = {
            'start': self.format_date(*start_date),
            'end': self.format_date(*end_date),
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
    # Meminta input dari pengguna
    start_year, start_month, start_day = input("Masukkan tanggal mulai (YYYY MM DD): ").split()
    end_year, end_month, end_day = input("Masukkan tanggal akhir (YYYY MM DD): ").split()
    try:
        data = api.get_reports((start_year, start_month, start_day), (end_year, end_month, end_day))
        # Tentukan direktori dan nama file
        directory = "C:\\c.PetaBencana\\Data"
        filename = "laporan_petabencana.json"
        # Simpan data ke dalam file
        api.save_to_file(data, directory, filename)
    except Exception as e:
        print(str(e))
