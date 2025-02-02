import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------------------
# Load Data & Konversi Tanggal
# ---------------------------
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# ---------------------------
# Judul Aplikasi
# ---------------------------
st.title("Bike Sharing Dashboard")

# ---------------------------
# Fitur Filtering Berdasarkan Rentang Tanggal
# ---------------------------
st.sidebar.header("Filter Data Berdasarkan Tanggal")
start_date = st.sidebar.date_input(
    "Start Date",
    value=datetime(2011, 1, 1),
    min_value=datetime(2011, 1, 1),
    max_value=datetime(2012, 12, 31)
)
end_date = st.sidebar.date_input(
    "End Date",
    value=datetime(2012, 12, 31),
    min_value=datetime(2011, 1, 1),
    max_value=datetime(2012, 12, 31)
)

# Validasi rentang tanggal
if start_date > end_date:
    st.error("Start Date harus sebelum End Date!")
    st.stop()

# Filter data pada kedua dataset berdasarkan tanggal yang dipilih
filtered_day = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) &
                      (day_df['dteday'] <= pd.to_datetime(end_date))]
filtered_hour = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) &
                        (hour_df['dteday'] <= pd.to_datetime(end_date))]

# Menampilkan jumlah data yang tersedia setelah filtering
st.write(f"Data 'day' dari {start_date} sampai {end_date}: {filtered_day.shape[0]} baris")
st.write(f"Data 'hour' dari {start_date} sampai {end_date}: {filtered_hour.shape[0]} baris")

# ---------------------------
# Visualisasi 1: Hourly Bike Rental Trend
# ---------------------------
st.subheader("Hourly Bike Rental Trend")
# Hitung rata-rata penyewaan per jam dari data yang telah difilter
hourly_trend = filtered_hour.groupby('hr')['cnt'].mean()

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(hourly_trend.index, hourly_trend.values, marker='o', linestyle='-')
ax1.set_xlabel('Jam dalam Sehari')
ax1.set_ylabel('Rata-rata Jumlah Penyewaan')
ax1.set_title('Tren Penyewaan Sepeda Berdasarkan Jam')
ax1.set_xticks(range(24))
ax1.grid(True)
st.pyplot(fig1)

# ---------------------------
# Visualisasi 2: Korelasi antara Cuaca dan Penyewaan Sepeda
# ---------------------------
st.subheader("Weather vs Bike Rental Correlation")
# Pastikan terdapat data untuk periode yang dipilih
if filtered_day.empty:
    st.write("Tidak ada data untuk periode yang dipilih.")
else:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    corr = filtered_day[['temp', 'hum', 'windspeed', 'cnt']].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax2)
    ax2.set_title("Korelasi antara Cuaca dan Penyewaan Sepeda")
    st.pyplot(fig2)
