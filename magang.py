import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File CSV tempat menyimpan data
FILE_PATH = "data.csv"

# Pastikan file CSV ada
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["id", "tanggal", "deskripsi_pekerjaan", "deskripsi_pengeluaran",
                                "jumlah_barang", "unit", "harga_per_satuan", "total_harga", "keterangan"])
    df.to_csv(FILE_PATH, index=False)
else:
    df = pd.read_csv(FILE_PATH)

# Fungsi membuat ID Transaksi
def generate_id_transaksi(kode_pelanggan, tanggal, df):
    tanggal_str = tanggal.strftime("%d%m%Y")
    urutan = len(df) + 1
    return f"{kode_pelanggan[:1].upper()}{tanggal_str}{urutan:02d}"

# Fungsi menyimpan data
def save_data(row):
    global df
    new_df = pd.DataFrame([row], columns=df.columns)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

# Fungsi mengedit data
def edit_data(index, new_row):
    global df
    df.iloc[index] = new_row
    df.to_csv(FILE_PATH, index=False)

# Fungsi menghapus data
def delete_data(index):
    global df
    df.drop(index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(FILE_PATH, index=False)

# UI Streamlit
st.title("Manajemen Data Transaksi")
st.header("Input Data Baru")

kode_pelanggan = st.text_input("Kode Pelanggan")
tanggal = st.date_input("Tanggal", value=datetime.today())
deskripsi_pekerjaan = st.text_input("Deskripsi Pekerjaan")
deskripsi_pengeluaran = st.text_input("Deskripsi Pengeluaran")
jumlah_barang = st.number_input("Jumlah Barang", min_value=0, step=1)
unit = st.text_input("Unit")
harga_per_satuan = st.number_input("Harga per Satuan", min_value=0, step=100)
total_harga = jumlah_barang * harga_per_satuan
keterangan = st.text_input("Keterangan")

if st.button("Simpan Data"):
    if not kode_pelanggan:
        st.error("Kode Pelanggan harus diisi.")
    else:
        tanggal_db = tanggal.strftime("%Y-%m-%d")
        id_transaksi = generate_id_transaksi(kode_pelanggan, tanggal, df)
        row = (id_transaksi, tanggal_db, deskripsi_pekerjaan, deskripsi_pengeluaran,
               jumlah_barang, unit, harga_per_satuan, total_harga, keterangan)
        save_data(row)
        st.success(f"Data ID {id_transaksi} berhasil disimpan!")

st.divider()
st.header("Kelola Data")

if len(df) > 0:
    df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')
    df_tampil = df.copy()
    df_tampil["tanggal"] = df_tampil["tanggal"].dt.strftime("%d-%m-%Y")
    st.dataframe(df_tampil)

    st.subheader("Edit / Hapus Data")
    idx = st.number_input("Pilih Index untuk Edit/Hapus", min_value=0, max_value=len(df)-1, step=1)
    selected_row = df.iloc[idx]

    with st.expander("Edit Data Ini"):
        tanggal_value = pd.to_datetime(selected_row['tanggal'], errors='coerce')
        if pd.isna(tanggal_value):
            tanggal_value = datetime.today()

        new_tanggal = st.date_input("Tanggal", value=tanggal_value)
        new_row = [
            selected_row['id'],
            new_tanggal.strftime("%Y-%m-%d"),
            st.text_input("Deskripsi Pekerjaan", value=selected_row['deskripsi_pekerjaan']),
            st.text_input("Deskripsi Pengeluaran", value=selected_row['deskripsi_pengeluaran']),
            st.number_input("Jumlah Barang", min_value=0, value=int(selected_row['jumlah_barang']), step=1),
            st.text_input("Unit", value=selected_row['unit']),
            st.number_input("Harga per Satuan", min_value=0, value=int(selected_row['harga_per_satuan']), step=100),
            selected_row['jumlah_barang'] * selected_row['harga_per_satuan'],
            st.text_input("Keterangan", value=selected_row['keterangan'])
        ]

        if st.button("Update Data"):
            edit_data(idx, new_row)
            st.success("Data berhasil diperbarui!")

    if st.button("Hapus Data Ini"):
        delete_data(idx)
        st.success("Data berhasil dihapus!")
else:
    st.info("Belum ada data.")
