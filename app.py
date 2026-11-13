"""Dashboard kunjungan wisata (2018-2025) dengan Flask + Pandas + Chart.js.

Jalankan:
    pip install -r requirements.txt
    python app.py
lalu buka http://127.0.0.1:5000
"""
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Data sudah dibersihkan di Google Colab. Baris '-' pada data asli = NaN (kosong).
df = pd.read_csv("data/data_wisatawan.csv")

NAMA_BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
              "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def filter_data(abaikan_tahun=False):
    """Terapkan filter ?tahun=2022 dan ?objek=Waduk Mrica (keduanya opsional)."""
    data = df
    tahun = request.args.get("tahun", type=int)
    objek = request.args.get("objek", type=str)
    if tahun and not abaikan_tahun:
        data = data[data["tahun"] == tahun]
    if objek:
        data = data[data["objek"] == objek]
    return data


def angka(x):
    """NaN tidak valid di JSON, jadi ubah menjadi 0."""
    return 0 if pd.isna(x) else round(float(x), 1)


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        daftar_tahun=sorted(df["tahun"].unique().tolist()),
        daftar_objek=sorted(df["objek"].unique().tolist()),
    )


@app.route("/api/ringkasan")
def ringkasan():
    data = filter_data()
    total = data["pengunjung"].sum()
    per_objek = data.groupby("objek")["pengunjung"].sum()
    teratas = per_objek.idxmax() if per_objek.sum() > 0 else "-"
    rata = data["pengunjung"].mean()  # NaN dilewati otomatis

    puncak = data.loc[data["pengunjung"].idxmax()] if data["pengunjung"].notna().any() else None
    return jsonify(
        total=int(total),
        objek_teratas=teratas,
        rata_bulanan=int(angka(rata)),
        puncak=(f"{NAMA_BULAN[int(puncak['bulan_no']) - 1]} {int(puncak['tahun'])}"
                if puncak is not None else "-"),
        bulan_kosong=int(data["pengunjung"].isna().sum()),
        baris=len(data),
    )


@app.route("/api/tren-tahun")
def tren_tahun():
    # Tren memperlihatkan semua tahun, jadi filter tahun diabaikan.
    hasil = filter_data(abaikan_tahun=True).groupby("tahun")["pengunjung"].sum()
    return jsonify(labels=[str(t) for t in hasil.index], data=[int(v) for v in hasil])


@app.route("/api/top-objek")
def top_objek():
    hasil = filter_data().groupby("objek")["pengunjung"].sum().sort_values(ascending=False)
    return jsonify(labels=hasil.index.tolist(), data=[int(v) for v in hasil])


@app.route("/api/musiman")
def musiman():
    hasil = filter_data().groupby("bulan_no")["pengunjung"].mean().reindex(range(1, 13))
    return jsonify(labels=NAMA_BULAN, data=[angka(v) for v in hasil])


@app.route("/api/komposisi")
def komposisi():
    hasil = filter_data().groupby("objek")["pengunjung"].sum().sort_values(ascending=False)
    lima = hasil.head(5)
    lainnya = hasil.iloc[5:].sum()
    labels, data = lima.index.tolist(), [int(v) for v in lima]
    if lainnya > 0:
        labels.append("Lainnya")
        data.append(int(lainnya))
    return jsonify(labels=labels, data=data)


if __name__ == "__main__":
    app.run(debug=True)
