# Dashboard Kunjungan Objek Wisata 2018-2025

Aplikasi visualisasi data berbasis web yang dibuat dengan **Flask**, **Pandas**, dan **Chart.js**. Dashboard menampilkan jumlah pengunjung bulanan di 12 objek wisata pada periode 2018 sampai 2025, lengkap dengan filter tahun dan objek wisata.

## Fitur

- Kartu ringkasan: total pengunjung, objek terpopuler, rata-rata per bulan, dan bulan puncak.
- Grafik garis: total pengunjung per tahun.
- Grafik batang horizontal: objek wisata dengan pengunjung terbanyak.
- Grafik donat: komposisi lima objek teratas (sisanya digabung sebagai "Lainnya").
- Grafik batang: pola musiman (rata-rata pengunjung per bulan).
- Filter tahun dan objek wisata yang memperbarui seluruh kartu dan grafik tanpa memuat ulang halaman.
- Catatan otomatis tentang jumlah bulan tanpa catatan pada pilihan filter.

## Teknologi

| Bagian | Teknologi |
|---|---|
| Backend | Python, Flask |
| Pengolahan data | Pandas |
| Visualisasi | Chart.js (dimuat dari CDN) |
| Tampilan | HTML dan CSS |

## Struktur Proyek

```
wisata-flask/
├── app.py                      # Backend Flask: route dan endpoint API
├── requirements.txt            # Daftar library
├── data/
│   └── data_wisatawan.csv      # Data hasil pembersihan
├── templates/
│   └── dashboard.html          # Halaman dashboard
└── docs/
    └── screenshot.png          # Tangkapan layar (opsional)
```

## Cara Menjalankan

Pastikan Python sudah terpasang, lalu jalankan perintah berikut dari folder proyek.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python app.py
```

Buka http://127.0.0.1:5000 di browser. Chart.js dimuat dari CDN, jadi perlu koneksi internet.

## Endpoint

| URL | Isi | Jenis grafik |
|---|---|---|
| `/` | Halaman dashboard | - |
| `/api/ringkasan` | Total, objek terpopuler, rata-rata per bulan, bulan puncak, jumlah bulan kosong | Kartu |
| `/api/tren-tahun` | Total pengunjung per tahun | Garis |
| `/api/top-objek` | Total pengunjung per objek, urut terbesar | Batang horizontal |
| `/api/komposisi` | Lima objek teratas dan "Lainnya" | Donat |
| `/api/musiman` | Rata-rata pengunjung per bulan | Batang |

Semua endpoint `/api/...` menerima filter opsional, misalnya:

```
/api/ringkasan?tahun=2020
/api/top-objek?tahun=2024&objek=Dataran Tinggi Dieng
```

Endpoint `/api/tren-tahun` hanya terpengaruh filter `objek`, karena grafik tren memang menampilkan semua tahun.

## Data dan Pembersihan

Data asli berisi 1.032 baris (bulan, objek wisata, jumlah pengunjung, tahun) dengan pemisah titik koma. Pembersihan dilakukan di Google Colab sebelum data dipakai di Flask.

Masalah yang ditemukan dan penanganannya:

1. **Tanda "-" pada 167 baris.** Disimpan sebagai nilai kosong (NaN), tidak dibuang dan tidak diisi 0. Fungsi `sum()` dan `mean()` Pandas melewati nilai kosong secara otomatis.
2. **Label bulan tidak konsisten.** Nama bulan bercampur bahasa Indonesia dan Inggris, dan pada tahun 2025 terdapat 33 label bulan yang tidak sesuai urutan. Bulan ditentukan dari urutan baris data, bukan dari teks labelnya.
3. **Label tahun salah pada 2 baris.** Diperbaiki dengan cara yang sama, yaitu berdasarkan urutan baris.
4. **Tipe data.** Kolom jumlah pengunjung diubah menjadi angka dengan `pd.to_numeric`.

Hasil akhir: 1.032 baris dan 4 kolom (`tahun`, `bulan_no`, `objek`, `pengunjung`) tanpa duplikat.

## Keterbatasan Data

- Makna tanda "-" adalah asumsi (objek tutup atau tidak tercatat). Dokumentasi dataset tidak menjelaskannya.
- Serayu Park dan Serayu Advanture Indonesia hanya memiliki catatan pada tahun 2018, 2019, dan 2025.
- Pada tahun 2025, data Surya Yudha Park identik dengan Surya Yudha Sport Centre pada 11 bulan, demikian pula Pikas Banyu Wong dengan Serayu Advanture Indonesia. Kemungkinan terjadi kesalahan penyalinan di sumber data, sehingga kenaikan total tahun 2025 perlu ditafsirkan dengan hati-hati.
- Untuk objek yang seluruh catatannya kosong pada suatu tahun, total ditampilkan 0 walaupun artinya "tidak tercatat".
- "Bulan puncak" pada kartu ringkasan adalah catatan tertinggi (satu objek pada satu bulan), bukan bulan dengan total gabungan tertinggi.

## Catatan

Mode `debug=True` pada `app.py` hanya untuk pengembangan. Nonaktifkan sebelum aplikasi dipublikasikan.
