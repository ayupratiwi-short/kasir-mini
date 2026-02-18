import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid

st.set_page_config(page_title="Kasir Mini Pink 💗", layout="wide")

# ===============================
# STYLE PINK
# ===============================
st.markdown("""
    <style>
    .stApp {
        background-color: #ffe6f2;
    }
    h1, h2, h3 {
        color: #d63384;
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# BUAT FILE JIKA BELUM ADA
# ===============================
if not os.path.exists("produk.csv"):
    pd.DataFrame(columns=["Nama", "Harga"]).to_csv("produk.csv", index=False)

if not os.path.exists("transaksi.csv"):
    pd.DataFrame(columns=[
        "ID","Tanggal","Hari","Jam",
        "Nama","Harga","Jumlah","Total","Status"
    ]).to_csv("transaksi.csv", index=False)

produk = pd.read_csv("produk.csv")
transaksi = pd.read_csv("transaksi.csv")

# ===============================
# PERBAIKI FILE LAMA (ANTI ERROR)
# ===============================
kolom_wajib = ["ID","Tanggal","Hari","Jam","Nama","Harga","Jumlah","Total","Status"]

for kolom in kolom_wajib:
    if kolom not in transaksi.columns:
        transaksi[kolom] = ""

transaksi.to_csv("transaksi.csv", index=False)

# ===============================
# TAB
# ===============================
tab1, tab2, tab3 = st.tabs(["🛍 Kelola Produk", "💳 Kasir", "📊 Laporan"])

# =====================================================
# TAB 1 PRODUK
# =====================================================
with tab1:
    st.header("Tambah Produk")

    nama = st.text_input("Nama Produk")
    harga = st.number_input("Harga", min_value=0)

    if st.button("Tambah Produk"):
        if nama != "":
            produk_baru = pd.DataFrame([[nama, harga]], columns=["Nama","Harga"])
            produk = pd.concat([produk, produk_baru], ignore_index=True)
            produk.to_csv("produk.csv", index=False)
            st.success("Produk berhasil ditambahkan 💗")

    st.subheader("Daftar Produk")

    if not produk.empty:
        st.dataframe(produk)

        hapus_produk = st.selectbox("Pilih produk untuk dihapus", produk["Nama"])
        if st.button("Hapus Produk"):
            produk = produk[produk["Nama"] != hapus_produk]
            produk.to_csv("produk.csv", index=False)
            st.success("Produk dihapus ✨")

# =====================================================
# TAB 2 KASIR
# =====================================================
with tab2:
    st.header("Kasir")

    if "keranjang" not in st.session_state:
        st.session_state.keranjang = []

    if not produk.empty:
        pilih_produk = st.selectbox("Pilih Produk", produk["Nama"])
        jumlah = st.number_input("Jumlah", min_value=1, value=1)

        if st.button("Tambah ke Keranjang"):
            harga = produk[produk["Nama"] == pilih_produk]["Harga"].values[0]
            st.session_state.keranjang.append({
                "Nama": pilih_produk,
                "Harga": harga,
                "Jumlah": jumlah,
                "Total": harga * jumlah
            })

    st.subheader("Keranjang")

    if st.session_state.keranjang:
        df_keranjang = pd.DataFrame(st.session_state.keranjang)
        st.dataframe(df_keranjang)

        total_bayar = df_keranjang["Total"].sum()
        st.subheader(f"Total: Rp {total_bayar}")

        if st.button("Proses Bayar 💰"):
            now = datetime.now()
            id_transaksi = str(uuid.uuid4())[:8]
            hari_indo = now.strftime("%A")

            hari_dict = {
                "Monday":"Senin","Tuesday":"Selasa","Wednesday":"Rabu",
                "Thursday":"Kamis","Friday":"Jumat","Saturday":"Sabtu","Sunday":"Minggu"
            }

            hari_indo = hari_dict.get(hari_indo, hari_indo)

            for item in st.session_state.keranjang:
                data_baru = pd.DataFrame([[
                    id_transaksi,
                    now.strftime("%Y-%m-%d"),
                    hari_indo,
                    now.strftime("%H:%M:%S"),
                    item["Nama"],
                    item["Harga"],
                    item["Jumlah"],
                    item["Total"],
                    "Berhasil"
                ]], columns=kolom_wajib)

                transaksi = pd.concat([transaksi, data_baru], ignore_index=True)

            transaksi.to_csv("transaksi.csv", index=False)
            st.session_state.keranjang = []
            st.success("Pembayaran Berhasil 💗")

# =====================================================
# TAB 3 LAPORAN
# =====================================================
with tab3:
    st.header("Laporan Penjualan")

    if not transaksi.empty:

        tanggal_pilih = st.selectbox("Pilih Tanggal", transaksi["Tanggal"].unique())
        data_hari = transaksi[
            (transaksi["Tanggal"] == tanggal_pilih) &
            (transaksi["Status"] == "Berhasil")
        ]

        st.subheader("Detail Transaksi")
        st.dataframe(data_hari)

        total_harian = data_hari["Total"].sum()
        st.subheader(f"Total Harian: Rp {total_harian}")

        # TOTAL BULANAN
        transaksi["Bulan"] = pd.to_datetime(transaksi["Tanggal"]).dt.to_period("M")
        bulan_pilih = st.selectbox("Pilih Bulan", transaksi["Bulan"].astype(str).unique())

        data_bulan = transaksi[
            (transaksi["Bulan"].astype(str) == bulan_pilih) &
            (transaksi["Status"] == "Berhasil")
        ]

        total_bulanan = data_bulan["Total"].sum()
        st.subheader(f"Total Bulanan: Rp {total_bulanan}")

        # DOWNLOAD EXCEL
        st.download_button(
            "Download Laporan Excel 📥",
            data_hari.to_csv(index=False),
            file_name="laporan_harian.csv",
            mime="text/csv"
        )
