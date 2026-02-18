import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kasir Ayu 💖", layout="centered")

st.title("🛍️ Kasir Ayu 💖")

# =============================
# FILE PRODUK
# =============================
if not os.path.exists("produk.csv"):
    df_produk = pd.DataFrame(columns=["Nama", "Harga"])
    df_produk.to_csv("produk.csv", index=False)

df_produk = pd.read_csv("produk.csv")

# =============================
# TAMBAH PRODUK
# =============================
st.subheader("➕ Tambah Produk")

nama_baru = st.text_input("Nama Produk")
harga_baru = st.number_input("Harga", min_value=0)

if st.button("Tambah Produk"):
    if nama_baru != "":
        df_produk.loc[len(df_produk)] = [nama_baru, harga_baru]
        df_produk.to_csv("produk.csv", index=False)
        st.success("Produk berhasil ditambahkan 💖")
        st.rerun()

# =============================
# HAPUS PRODUK
# =============================
st.subheader("🗑️ Hapus Produk")

if not df_produk.empty:
    pilih_produk = st.selectbox("Pilih produk", df_produk["Nama"])

    if st.button("Hapus Produk ❌"):
        df_produk = df_produk[df_produk["Nama"] != pilih_produk]
        df_produk.to_csv("produk.csv", index=False)
        st.success("Produk berhasil dihapus 💖")
        st.rerun()
else:
    st.write("Belum ada produk.")

# =============================
# KERANJANG
# =============================
st.subheader("🛒 Keranjang")

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

if not df_produk.empty:
    produk_pilih = st.selectbox("Pilih Produk untuk dibeli", df_produk["Nama"])
    jumlah = st.number_input("Jumlah", min_value=1, step=1)

    if st.button("Tambah ke Keranjang"):
        harga = df_produk[df_produk["Nama"] == produk_pilih]["Harga"].values[0]
        total = harga * jumlah
        st.session_state.keranjang.append(
            {"Nama": produk_pilih, "Jumlah": jumlah, "Total": total}
        )
        st.success("Ditambahkan ke keranjang 💖")

# Tampilkan isi keranjang
if st.session_state.keranjang:
    df_keranjang = pd.DataFrame(st.session_state.keranjang)
    st.dataframe(df_keranjang)

    total_bayar = df_keranjang["Total"].sum()
    st.write(f"### 💰 Total Bayar: Rp {total_bayar}")

    if st.button("Bayar Sekarang 💖"):
        waktu = datetime.now()

        data_transaksi = pd.DataFrame([{
            "Tanggal": waktu,
            "Total": total_bayar
        }])

        if os.path.exists("transaksi.csv"):
            data_lama = pd.read_csv("transaksi.csv")
            data_transaksi = pd.concat([data_lama, data_transaksi])

        data_transaksi.to_csv("transaksi.csv", index=False)

        st.success("Transaksi berhasil 💖")
        st.session_state.keranjang = []
        st.rerun()

# =============================
# LAPORAN HARI INI
# =============================
st.
