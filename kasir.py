import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# =======================
# STYLE PINK 💗
# =======================
st.markdown("""
<style>
.stApp {background-color: #ffe6f2;}
h1, h2, h3 {color: #ff3399;}
</style>
""", unsafe_allow_html=True)

st.title("🛒💗 Kasir Mini 💗")

menu = st.sidebar.selectbox("Menu", ["Kasir", "Tambah Produk"])

# =======================
# SESSION KERANJANG
# =======================
if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

# =======================
# TAMBAH PRODUK
# =======================
if menu == "Tambah Produk":
    st.subheader("➕ Tambah Produk")

    nama = st.text_input("Nama Produk")
    harga = st.number_input("Harga", min_value=0)

    if st.button("Simpan Produk"):
        data = pd.DataFrame([{"Nama": nama, "Harga": harga}])

        if os.path.exists("produk.csv"):
            data.to_csv("produk.csv", mode='a', header=False, index=False)
        else:
            data.to_csv("produk.csv", index=False)

        st.success("Produk berhasil ditambahkan 💗")
    st.subheader("🗑️ Hapus Produk")

if os.path.exists("produk.csv"):
    data_produk = pd.read_csv("produk.csv")

    if not data_produk.empty:
        pilih_produk = st.selectbox(
            "Pilih produk yang ingin dihapus",
            data_produk["Nama"]
        )

        if st.button("Hapus Produk ❌"):
            data_produk = data_produk[data_produk["Nama"] != pilih_produk]
            data_produk.to_csv("produk.csv", index=False)
            st.success("Produk berhasil dihapus 💗")
            st.rerun()
    else:
        st.write("Belum ada produk.")
else:
    st.write("File produk belum ada.")


# =======================
# KASIR
# =======================
elif menu == "Kasir":
    st.subheader("💳 Transaksi")

    if os.path.exists("produk.csv"):
        produk = pd.read_csv("produk.csv")

        pilih = st.selectbox("Pilih Produk", produk["Nama"])
        jumlah = st.number_input("Jumlah", min_value=1)

        harga = produk[produk["Nama"] == pilih]["Harga"].values[0]
        subtotal = harga * jumlah

        st.write("Harga:", harga)
        st.write("Subtotal:", subtotal)

        if st.button("Tambah ke Keranjang 💗"):
            st.session_state.keranjang.append({
                "Produk": pilih,
                "Harga": harga,
                "Jumlah": jumlah,
                "Total": subtotal
            })
            st.success("Ditambahkan ke keranjang!")

        # =======================
        # TAMPILKAN KERANJANG
        # =======================
        if st.session_state.keranjang:
            st.subheader("🛍 Keranjang")

            for i, item in enumerate(st.session_state.keranjang):
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.write(item["Produk"])
                col2.write(item["Harga"])
                col3.write(item["Jumlah"])
                col4.write(item["Total"])

                if col5.button("❌", key=f"hapus_{i}"):
                    st.session_state.keranjang.pop(i)
                    st.rerun()

            df_keranjang = pd.DataFrame(st.session_state.keranjang)
            total_bayar = df_keranjang["Total"].sum()

            st.write("### 💰 Total Bayar:", total_bayar)

            colA, colB = st.columns(2)

            if colA.button("💖 Bayar"):
                tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df_keranjang["Tanggal"] = tanggal

                if os.path.exists("transaksi.csv"):
                    df_keranjang.to_csv("transaksi.csv", mode='a', header=False, index=False)
                else:
                    df_keranjang.to_csv("transaksi.csv", index=False)

                st.success("Pembayaran berhasil 💗")
                st.session_state.keranjang = []
                st.rerun()

            if colB.button("🗑 Kosongkan"):
                st.session_state.keranjang = []
                st.warning("Keranjang dikosongkan!")
                st.rerun()

        # =======================
        # LAPORAN HARI INI
        # =======================
        st.subheader("📊 Penjualan Hari Ini")

        if os.path.exists("transaksi.csv"):
            data = pd.read_csv("transaksi.csv")

            if not data.empty:
                data["Tanggal"] = pd.to_datetime(data["Tanggal"])
                hari_ini = datetime.now().date()
                data_hari_ini = data[data["Tanggal"].dt.date == hari_ini]

                total_harian = data_hari_ini["Total"].sum()
                st.write("Total Hari Ini:", total_harian)

                # Grafik per jam
                if not data_hari_ini.empty:
                    data_hari_ini["Jam"] = data_hari_ini["Tanggal"].dt.strftime("%H:%M")
                    per_jam = data_hari_ini.groupby("Jam")["Total"].sum()

                    st.write("### 📈 Grafik Penjualan")
                    fig, ax = plt.subplots()
                    ax.plot(per_jam.index, per_jam.values)
                    ax.set_xlabel("Jam")
                    ax.set_ylabel("Total")
                    ax.set_title("Penjualan Per Jam Hari Ini")
                    st.pyplot(fig)

        # =======================
        # BATALKAN TRANSAKSI
        # =======================
        st.subheader("🚨 Batalkan Transaksi")

        if os.path.exists("transaksi.csv"):
            data = pd.read_csv("transaksi.csv")

            if not data.empty:
                pilih_index = st.selectbox(
                    "Pilih index transaksi yang ingin dibatalkan",
                    data.index
                )

                if st.button("❌ Batalkan"):
                    data = data.drop(pilih_index)
                    data.to_csv("transaksi.csv", index=False)
                    st.success("Transaksi dibatalkan 💗")
                    st.rerun()

    else:
        st.warning("Belum ada produk 💗 Tambahkan dulu ya.")




