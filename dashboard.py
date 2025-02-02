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
st.title("Bike Sharing Data Analysis")

# ---------------------------
# Fitur Filtering Interaktif
# ---------------------------
# 1. Filter berdasarkan rentang tanggal untuk kedua dataset
st.subheader("Filter Berdasarkan Tanggal")
start_date = st.date_input(
    'Start Date', 
    value=datetime(2011, 1, 1), 
    min_value=datetime(2011, 1, 1), 
    max_value=datetime(2012, 12, 31)
)
end_date = st.date_input(
    'End Date', 
    value=datetime(2012, 12, 31), 
    min_value=datetime(2011, 1, 1), 
    max_value=datetime(2012, 12, 31)
)

# Pastikan end_date tidak lebih kecil dari start_date
if start_date > end_date:
    st.error("Start Date harus sebelum End Date!")
    st.stop()

# Filter data berdasarkan tanggal
filtered_day = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) &
                      (day_df['dteday'] <= pd.to_datetime(end_date))]
filtered_hour = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) &
                        (hour_df['dteday'] <= pd.to_datetime(end_date))]

# 2. Filter berdasarkan musim (Season)
st.subheader("Filter Berdasarkan Musim")
# Opsi 0 berarti "All" (tidak difilter)
season_filter = st.selectbox(
    "Select Season", 
    options=[0, 1, 2, 3, 4], 
    format_func=lambda x: "All" if x == 0 else ['Spring', 'Summer', 'Fall', 'Winter'][x-1]
)
if season_filter != 0:
    filtered_day = filtered_day[filtered_day['season'] == season_filter]
    filtered_hour = filtered_hour[filtered_hour['season'] == season_filter]

# 3. Filter berdasarkan kondisi cuaca (weathersit)
st.subheader("Filter Berdasarkan Kondisi Cuaca")
weather_filter = st.selectbox(
    "Select Weather Situation", 
    options=[0, 1, 2, 3], 
    format_func=lambda x: "All" if x == 0 else ['Clear', 'Mist', 'Heavy Rain'][x-1]
)
if weather_filter != 0:
    filtered_day = filtered_day[filtered_day['weathersit'] == weather_filter]
    filtered_hour = filtered_hour[filtered_hour['weathersit'] == weather_filter]

# Tampilkan jumlah data yang tersisa setelah filtering
st.write("Jumlah data (day dataset):", filtered_day.shape[0])
st.write("Jumlah data (hour dataset):", filtered_hour.shape[0])

# ---------------------------
# Visualisasi: Hourly Bike Rental Trend
# ---------------------------
st.subheader("Hourly Bike Rental Trend")
# Menghitung rata-rata penyewaan per jam dari dataset hour yang sudah difilter
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
# Visualisasi: Korelasi antara Cuaca dan Penyewaan Sepeda
# ---------------------------
st.subheader("Weather vs Bike Rental Correlation")
# Pastikan data yang digunakan untuk korelasi memiliki jumlah baris > 0
if filtered_day.shape[0] > 0:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    corr = filtered_day[['temp', 'hum', 'windspeed', 'cnt']].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax2)
    ax2.set_title("Korelasi antara Cuaca dan Penyewaan Sepeda")
    st.pyplot(fig2)
else:
    st.write("Tidak ada data yang tersedia untuk periode dan filter yang dipilih.")

# ---------------------------
# Statistik Deskriptif
# ---------------------------
st.subheader("Descriptive Statistics (Day Dataset)")
st.write(filtered_day.describe())
