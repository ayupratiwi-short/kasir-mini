import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Kasir Ayu 💖", layout="centered")

st.title("🛍️ Kasir Ayu 💖")

# =============================
# BUAT FILE PRODUK
# =============================
if not os.path.exists("produk.csv"):
    pd.DataFrame(columns=["Nama", "Harga"]).to_csv("produk.csv", index=False)

df_produk = pd.read_csv("produk.csv")

# =============================
# BUAT FILE TRANSAKSI
# =============================
if not os.path.exists("transaksi.csv"):
    pd.DataFrame(columns=[
        "ID", "Tanggal", "Hari", "Jam",
        "Nama", "Harga", "Jumlah",
        "Total", "Status"
    ]).to_csv("transaksi.csv", index=False)

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
        pilih_produk = st.selectbox("Pilih produk", df_produk["Nama"])

        if st.button("Hapus Produk ❌"):
            df_produk = df_produk[df_produk["Nama"] != pilih_produk]
            df_produk.to_csv("produk.csv", index=False)
            st.success("Produk berhasil dihapus 💖")
            st.rerun()

# =====================================================
# TAB 2 - KASIR & LAPORAN
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
                "Harga": harga,
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

            hari_inggris = now.strftime("%A")
            translate_hari = {
                "Monday": "Senin",
                "Tuesday": "Selasa",
                "Wednesday": "Rabu",
                "Thursday": "Kamis",
                "Friday": "Jumat",
                "Saturday": "Sabtu",
                "Sunday": "Minggu"
            }
            hari = translate_hari[hari_inggris]

            jam = now.strftime("%H:%M:%S")
            transaksi_id = now.strftime("%Y%m%d%H%M%S")

            data_list = []

            for item in st.session_state.keranjang:
                data_list.append({
                    "ID": transaksi_id,
                    "Tanggal": tanggal,
                    "Hari": hari,
                    "Jam": jam,
                    "Nama": item["Nama"],
                    "Harga": item["Harga"],
                    "Jumlah": item["Jumlah"],
                    "Total": item["Total"],
                    "Status": "Berhasil"
                })

            data_baru = pd.DataFrame(data_list)
            data_lama = pd.read_csv("transaksi.csv")
            data_gabung = pd.concat([data_lama, data_baru])

            data_gabung.to_csv("transaksi.csv", index=False)

            st.success("Transaksi berhasil 💖")
            st.session_state.keranjang = []
            st.rerun()

    # =============================
    # LAPORAN PER HARI
    # =============================
    st.subheader("📊 Laporan Penjualan Per Hari")

    data = pd.read_csv("transaksi.csv")

    if not data.empty:

        data["Tanggal"] = pd.to_datetime(data["Tanggal"])
        daftar_tanggal = sorted(data["Tanggal"].dt.date.unique())

        pilih_tanggal = st.date_input(
            "Pilih Tanggal",
            value=daftar_tanggal[-1]
        )

        data_filter = data[data["Tanggal"].dt.date == pilih_tanggal]

        if not data_filter.empty:

            st.dataframe(data_filter)

            data_berhasil = data_filter[data_filter["Status"] == "Berhasil"]
            total_harian = data_berhasil["Total"].sum()

            st.write(f"### 💰 Total Penjualan Hari Ini: Rp {total_harian}")

            # VOID
            st.subheader("🚨 Batalkan Transaksi")

            daftar_id = data_filter[data_filter["Status"] == "Berhasil"]["ID"].unique()

            if len(daftar_id) > 0:
                pilih_id = st.selectbox("Pilih ID Transaksi", daftar_id)

                if st.button("Batalkan Transaksi ❌"):
                    data.loc[data["ID"] == pilih_id, "Status"] = "Void"
                    data.to_csv("transaksi.csv", index=False)
                    st.success("Transaksi berhasil dibatalkan 💖")
                    st.rerun()
            else:
                st.info("Tidak ada transaksi aktif.")

            # DOWNLOAD EXCEL
            st.subheader("📥 Download Laporan")

            file_excel = f"laporan_{pilih_tanggal}.xlsx"
            data_filter.to_excel(file_excel, index=False)

            with open(file_excel, "rb") as file:
                st.download_button(
                    label="Download Excel 💖",
                    data=file,
                    file_name=f"Laporan_{pilih_tanggal}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        else:
            st.info("Tidak ada transaksi di tanggal ini.")
    else:
        st.info("Belum ada transaksi.")

    # =============================
    # LAPORAN BULANAN
    # =============================
    st.subheader("📅 Laporan Penjualan Bulanan")

    if not data.empty:

        # Pastikan kolom tanggal dalam format datetime
        data["Tanggal"] = pd.to_datetime(data["Tanggal"])

        # Tambahkan kolom Bulan & Tahun
        data["Bulan"] = data["Tanggal"].dt.month
        data["Tahun"] = data["Tanggal"].dt.year

        daftar_bulan = sorted(data["Bulan"].unique())
        daftar_tahun = sorted(data["Tahun"].unique())

        col1, col2 = st.columns(2)

        with col1:
            pilih_bulan = st.selectbox("Pilih Bulan", daftar_bulan)

        with col2:
            pilih_tahun = st.selectbox("Pilih Tahun", daftar_tahun)

        data_bulan = data[
            (data["Bulan"] == pilih_bulan) &
            (data["Tahun"] == pilih_tahun)
        ]

        if not data_bulan.empty:

            st.dataframe(data_bulan)

            data_berhasil_bulan = data_bulan[data_bulan["Status"] == "Berhasil"]
            total_bulanan = data_berhasil_bulan["Total"].sum()

            st.write(f"### 💰 Total Penjualan Bulan Ini: Rp {total_bulanan}")

            # Download bulanan
            file_excel_bulan = f"laporan_{pilih_bulan}_{pilih_tahun}.xlsx"
            data_bulan.to_excel(file_excel_bulan, index=False)

            with open(file_excel_bulan, "rb") as file:
                st.download_button(
                    label="Download Laporan Bulanan 💖",
                    data=file,
                    file_name=f"Laporan_{pilih_bulan}_{pilih_tahun}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        else:
            st.info("Tidak ada transaksi di bulan ini.")



