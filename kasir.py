import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Kasir Ayu 💖", layout="centered")

st.title("🛍️ Kasir Ayu 💖")

# =============================
# BUAT FILE PRODUK JIKA BELUM ADA
# =============================
if not os.path.exists("produk.csv"):
    pd.DataFrame(columns=["Nama", "Harga"]).to_csv("produk.csv", index=False)

df_produk = pd.read_csv("produk.csv")

# =============================
# BUAT FILE TRANSAKSI JIKA BELUM ADA
# =============================
if not os.path.exists("transaksi.csv"):
    pd.DataFrame(columns=["Tanggal", "Hari", "Jam", "Total"]).to_csv("transaksi.csv", index=False)

# =============================
# TABS
# =============================
tab1, tab2 = st.tabs(["📦 Manajemen Produk", "🛒 Kasir & Laporan"])

# =====================================================
# TAB 1 - MANAJEMEN PRODUK
# =====================================================
with tab1:

    st.subheader("📋 Daftar Produk")
    if not df_produk.empty:
        st.dataframe(df_produk)
    else:
        st.info("Belum ada produk.")

    st.subheader("➕ Tambah Produk")

    nama_baru = st.text_input("Nama Produk")
    harga_baru = st.number_input("Harga", min_value=0)

    if st.button("Tambah Produk"):
        if nama_baru != "":
            df_produk.loc[len(df_produk)] = [nama_baru, harga_baru]
            df_produk.to_csv("produk.csv", index=False)
            st.success("Produk berhasil ditambahkan 💖")
            st.rerun()

    st.subheader("🗑️ Hapus Produk")

    if not df_produk.empty:
        pilih_produk = st.selectbox("Pilih produk yang ingin dihapus", df_produk["Nama"])

        if st.button("Hapus Produk ❌"):
            df_produk = df_produk[df_produk["Nama"] != pilih_produk]
            df_produk.to_csv("produk.csv", index=False)
            st.success("Produk berhasil dihapus 💖")
            st.rerun()

# =====================================================
# TAB 2 - KASIR + LAPORAN
# =====================================================
with tab2:

    st.subheader("🛒 Kasir")

    if "keranjang" not in st.session_state:
        st.session_state.keranjang = []

    if not df_produk.empty:
        produk_pilih = st.selectbox("Pilih Produk", df_produk["Nama"])
        jumlah = st.number_input("Jumlah", min_value=1, step=1)

        if st.button("Tambah ke Keranjang"):
            harga = df_produk[df_produk["Nama"] == produk_pilih]["Harga"].values[0]
            total = harga * jumlah

            st.session_state.keranjang.append({
                "Nama": produk_pilih,
                "Jumlah": jumlah,
                "Total": total
            })

            st.success("Ditambahkan ke keranjang 💖")

    # =============================
    # TAMPILKAN KERANJANG
    # =============================
    if st.session_state.keranjang:
        df_keranjang = pd.DataFrame(st.session_state.keranjang)
        st.dataframe(df_keranjang)

        total_bayar = df_keranjang["Total"].sum()
        st.write(f"### 💰 Total Bayar: Rp {total_bayar}")

        if st.button("Bayar Sekarang 💖"):

            now = datetime.now()

            tanggal = now.strftime("%Y-%m-%d")
            hari = now.strftime("%A")
            jam = now.strftime("%H:%M:%S")

            data_baru = pd.DataFrame([{
                "Tanggal": tanggal,
                "Hari": hari,
                "Jam": jam,
                "Total": total_bayar
            }])

            data_lama = pd.read_csv("transaksi.csv")
            data_gabung = pd.concat([data_lama, data_baru])

            data_gabung.to_csv("transaksi.csv", index=False)

            st.success("Transaksi berhasil 💖")
            st.session_state.keranjang = []
            st.rerun()

    # =============================
    # LAPORAN PENJUALAN
    # =============================
    st.subheader("📊 Laporan Penjualan")

    data = pd.read_csv("transaksi.csv")

    if not data.empty:
        st.dataframe(data)
    else:
        st.info("Belum ada transaksi.")
