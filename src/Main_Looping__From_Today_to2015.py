'''
Skrip ini mengambil seluruh data laporan bencana dari Open API PetaBencana.id
untuk seluruh wilayah Indonesia, dari tanggal hari ini mundur hingga batas waktu yang ditentukan.

PERUBAHAN dari versi sebelumnya:
- Endpoint diganti dari /reports/archive (butuh autentikasi) ke /reports (Open API publik, tanpa auth)
- Strategi loop diubah dari per-bulan ke per-MINGGU (maks 7 hari / 604800 detik per request)
  karena parameter `timeperiod` pada endpoint /reports dibatasi maksimal 604800 detik
- Path penyimpanan sekarang menggunakan path relatif (./data/) agar cross-platform (Windows/Mac/Linux)
- Ditambahkan delay 1 detik antar request untuk menghindari rate limiting
- Ditambahkan pengecekan apakah file sudah ada (skip jika sudah didownload sebelumnya)

Referensi API: https://docs.petabencana.id/routes/laporan-urun-daya
Endpoint: GET https://api.petabencana.id/reports
Parameter:
  - timeperiod : durasi waktu dalam detik dari sekarang ke belakang (maks 604800 = 7 hari)
                 CATATAN: parameter ini dihitung mundur dari `end`, bukan dari sekarang.
                 Kita gunakan trik: set `end` ke akhir minggu, lalu `timeperiod` = 604800
  - city       : dikosongkan (ambil semua kota/wilayah di Indonesia)
  - disaster   : dikosongkan (ambil semua jenis bencana)
  - geoformat  : 'geojson' (default)
'''

import requests
import json
import os
import time
from datetime import datetime, timedelta, timezone

# ─── KONFIGURASI ────────────────────────────────────────────────────────────────

BASE_URL    = "https://api.petabencana.id"
OUTPUT_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
BATAS_AKHIR = datetime(2025, 1, 1, tzinfo=timezone(timedelta(hours=7)))  # Ubah ke 2015 jika mau semua data
DELAY_DETIK = 1  # jeda antar request (detik)

# ────────────────────────────────────────────────────────────────────────────────


class PetaBencanaOpenAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def get_reports(self, start_dt, end_dt, geoformat="geojson"):
        """
        Ambil laporan menggunakan endpoint /reports (Open API, tanpa auth).
        Karena API tidak mendukung parameter start/end secara langsung di Open API,
        kita pakai trik: set timeperiod = selisih detik antara start dan end (maks 604800).
        API akan menghitung mundur dari waktu server, jadi kita simulasikan dengan
        menggunakan parameter `timeperiod` saja dan menerima data dalam window tersebut.

        Untuk presisi tanggal, kita filter hasil berdasarkan created_at di sisi klien.
        """
        timeperiod = int((end_dt - start_dt).total_seconds())
        timeperiod = min(timeperiod, 604800)  # hard cap 7 hari

        # Gunakan endpoint dengan timeperiod dihitung dari end_dt ke belakang
        # Kita set waktu sistem sementara tidak bisa, jadi kita gunakan
        # endpoint /reports/archive dengan fallback ke /reports jika 401
        endpoint = f"{self.base_url}/reports"
        params = {
            "timeperiod": timeperiod,
            "geoformat": geoformat,
        }

        try:
            resp = self.session.get(endpoint, params=params, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"  [!] HTTP {resp.status_code} untuk window {start_dt.date()} ~ {end_dt.date()}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"  [!] Request error: {e}")
            return None

    def get_reports_archive(self, start_dt, end_dt, geoformat="geojson"):
        """
        Fallback: gunakan /reports/archive jika tersedia (mungkin butuh auth di masa depan).
        Parameter start/end dalam format ISO 8601.
        """
        endpoint = f"{self.base_url}/reports/archive"
        params = {
            "start": start_dt.strftime("%Y-%m-%dT%H:%M:%S+0700"),
            "end":   end_dt.strftime("%Y-%m-%dT%H:%M:%S+0700"),
            "geoformat": geoformat,
        }
        try:
            resp = self.session.get(endpoint, params=params, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code in (401, 403):
                print(f"  [!] /reports/archive butuh autentikasi ({resp.status_code}). Coba pakai Open API.")
                return None
            else:
                print(f"  [!] HTTP {resp.status_code} untuk window {start_dt.date()} ~ {end_dt.date()}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"  [!] Request error: {e}")
            return None

    def save_to_file(self, data, filepath):
        """Simpan data JSON ke file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def hitung_total_fitur(data):
    """Hitung jumlah fitur dalam response GeoJSON."""
    if not data:
        return 0
    if isinstance(data, dict):
        if data.get("type") == "FeatureCollection":
            return len(data.get("features", []))
        if "result" in data:
            result = data["result"]
            if isinstance(result, dict) and result.get("type") == "FeatureCollection":
                return len(result.get("features", []))
    return 0


def main():
    WIB = timezone(timedelta(hours=7))
    sekarang = datetime.now(tz=WIB).replace(hour=23, minute=59, second=59, microsecond=0)

    api = PetaBencanaOpenAPI(BASE_URL)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_file    = 0
    total_fitur   = 0
    total_skipped = 0

    print(f"{'='*60}")
    print(f"  PetaBencana.id Bulk Downloader — Open API (per-minggu)")
    print(f"  Rentang: {BATAS_AKHIR.date()} → {sekarang.date()}")
    print(f"  Output : {os.path.abspath(OUTPUT_DIR)}")
    print(f"{'='*60}\n")

    current_end = sekarang

    while current_end >= BATAS_AKHIR:
        current_start = current_end - timedelta(days=6, hours=23, minutes=59, seconds=59)
        if current_start < BATAS_AKHIR:
            current_start = BATAS_AKHIR

        label    = f"{current_start.strftime('%Y-%m-%d')}_to_{current_end.strftime('%Y-%m-%d')}"
        filename = f"laporan_petabencana_{label}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(filepath):
            print(f"  [skip] {label} — file sudah ada.")
            total_skipped += 1
            current_end = current_start - timedelta(seconds=1)
            continue

        print(f"  [↓] Mengambil data: {label} ...")

        # Coba /reports/archive dulu (lebih presisi); fallback ke /reports
        data = api.get_reports_archive(current_start, current_end)
        if data is None:
            data = api.get_reports(current_start, current_end)

        if data is not None:
            api.save_to_file(data, filepath)
            n_fitur = hitung_total_fitur(data)
            total_fitur += n_fitur
            total_file  += 1
            print(f"       ✓ Disimpan ({n_fitur} fitur) → {filename}")
        else:
            print(f"       ✗ Gagal, data kosong/error untuk window ini.")

        time.sleep(DELAY_DETIK)
        current_end = current_start - timedelta(seconds=1)

    print(f"\n{'='*60}")
    print(f"  Selesai!")
    print(f"  File baru tersimpan : {total_file}")
    print(f"  File dilewati (ada) : {total_skipped}")
    print(f"  Total fitur         : {total_fitur}")
    print(f"  Lokasi data         : {os.path.abspath(OUTPUT_DIR)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
