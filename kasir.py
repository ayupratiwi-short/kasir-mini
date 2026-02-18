import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# STYLE PINK 💗
# =========================
st.markdown("""
    <style>
    .stApp {
        background-color: #ffe6f2;
    }
    h1, h2, h3 {
        color: #ff3399;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛒💗 Kasir Mini Cantik 💗")

menu = st.sidebar.selectbox("Menu", ["Kasir", "Tambah Produk"])

# =========================
# SESSION KERANJANG
# =========================
if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

# =========================
# TAMBAH PRODUK
# =========================
if menu == "Tambah Produk":
    st.subheader("➕ Tambah Produk Baru")

    nama_produk = st.text_input("Nama Produk")
    harga_produk = st.number_input("Harga Produk", min_value=0)

    if st.button("Simpan Produk"):
        data_produk = {"Nama": nama_produk, "Harga": harga_produk}
        df = pd.DataFrame([data_produk])

        if os.path.exists("produk.csv"):
            df.to_csv("produk.csv", mode='a', header=False, index=False)
        else:
            df.to_csv("produk.csv", index=False)

        st.success("Produk berhasil ditambahkan! 💗")

# =========================
# KASIR
# =========================
elif menu == "Kasir":
    st.subheader("💳 Transaksi")

    if os.path.exists("produk.csv"):
        produk = pd.read_csv("produk.csv")

        pilih_produk = st.selectbox("Pilih Produk", produk["Nama"])
        jumlah = st.number_input("Jumlah", min_value=1)

        harga = produk[produk["Nama"] == pilih_produk]["Harga"].values[0]
        total = harga * jumlah

        st.write(f"Harga: Rp {harga}")
        st.write(f"Subtotal: Rp {total}")

        if st.button("Tambah ke Keranjang 💗"):
            st.session_state.keranjang.append({
                "Produk": pilih_produk,
                "Harga": harga,
                "Jumlah": jumlah,
                "Total": total
            })
            st.success("Ditambahkan ke keranjang!")

        # =========================
        # TAMPILKAN KERANJANG
        # =========================
        if st.session_state.keranjang:
            st.subheader("🛍 Keranjang")

            df_keranjang = pd.DataFrame(st.session_state.keranjang)
            st.dataframe(df_keranjang)

            total_bayar = df_keranjang["Total"].sum()
            st.write("### 💰 Total Bayar: Rp", total_bayar)

            if st.button("Bayar Sekarang 💖"):
                tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                df_keranjang["Tanggal"] = tanggal

                if os.path.exists("transaksi.csv"):
                    df_keranjang.to_csv("transaksi.csv", mode='a', header=False, index=False)
                else:
                    df_keranjang.to_csv("transaksi.csv", index=False)

                st.success("Pembayaran berhasil! 💗")

                st.session_state.keranjang = []

        # =========================
        # LAPORAN HARI INI
        # =========================
        st.subheader("📊 Penjualan Hari Ini")

        if os.path.exists("transaksi.csv"):
            data = pd.read_csv("transaksi.csv")
            hari_ini = datetime.now().strftime("%Y-%m-%d")

            data_hari_ini = data[data["Tanggal"].str.contains(hari_ini)]

            total_harian = data_hari_ini["Total"].sum()

            st.write("Total Penjualan Hari Ini: Rp", total_harian)
        else:
            st.write("Belum ada transaksi hari ini.")

    else:
        st.warning("Belum ada produk. Tambahkan dulu yaa 💗")
