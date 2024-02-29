# Cara Menggunakan

## Ikhtisar
Panduan ini menyediakan instruksi langkah-demi-langkah tentang cara menggunakan skrip Python di repositori `PetaBencana.id_BulkDownloader` untuk mengunduh dan memproses data bencana dari API PetaBencana.id.

## Prasyarat
- Pastikan Anda telah menginstal Python 3.x di sistem Anda.
- Instal perpustakaan Python yang diperlukan dengan `pip install -r requirements.txt`.

## Langkah-Langkah

1. **Menyiapkan Lingkungan Anda**
   - Klon repositori menggunakan `git clone https://github.com/username-anda/PetaBencana.id_BulkDownloader.git`.
   - Navigasi ke folder repositori yang telah diklon.
   - Instal paket Python yang dibutuhkan: `pip install -r requirements.txt`.

2. **Mengonfigurasi Skrip**
   - Buka file `config.json` di direktori `src`.
   - Atur kunci API dan parameter konfigurasi lainnya sesuai kebutuhan.

3. **Menjalankan Skrip**
   - Jalankan skrip utama untuk memulai proses pengunduhan: `python Main.py`.
   - Untuk tugas-tugas tertentu, jalankan skrip yang sesuai, misalnya, `python Main_Combine_n_FlattenJSON.py`.

4. **Pengolahan Data**
   - Setelah pengunduhan, Anda dapat menjalankan `Main_Flatten_Json.py` untuk melicinkan struktur JSON.
   - Gunakan `Main_Json_to_Geojson.py` untuk mengonversi data ke format GeoJSON.

5. **Analisis Data**
   - Dengan data dalam format yang diinginkan, Anda sekarang dapat melanjutkan analisis Anda menggunakan alat seperti QGIS, ArcGIS, atau perangkat lunak analisis data lainnya yang mendukung GeoJSON.

Untuk informasi lebih rinci, lihat dokumentasi skrip individu dalam direktori `src`.

Terima kasih telah menggunakan `PetaBencana.id_BulkDownloader`.
