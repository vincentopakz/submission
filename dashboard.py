import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Memuat dataset
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Mengubah kolom 'dteday' menjadi tipe data datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Menambahkan filter tanggal
st.title("Bike Sharing Data Analysis")

start_date = st.date_input('Start Date', min_value=datetime(2011, 1, 1), max_value=datetime(2012, 12, 31))
end_date = st.date_input('End Date', min_value=datetime(2011, 1, 1), max_value=datetime(2012, 12, 31))

# Filter data berdasarkan tanggal
filtered_data = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

# Menampilkan data yang difilter
st.write(f"Data yang difilter antara {start_date} dan {end_date}")
st.write(filtered_data)

# Filter berdasarkan musim
season_filter = st.selectbox('Select Season', options=[1, 2, 3, 4], format_func=lambda x: ['Spring', 'Summer', 'Fall', 'Winter'][x-1])

# Filter data berdasarkan musim
season_data = filtered_data[filtered_data['season'] == season_filter]

# Menampilkan data yang difilter
st.write(f"Data untuk musim: {['Spring', 'Summer', 'Fall', 'Winter'][season_filter - 1]}")
st.write(season_data)

# Visualisasi Tren Penyewaan Sepeda Berdasarkan Jam
st.subheader('Hourly Bike Rental Trend')
hourly_trend = hour_df.groupby('hr')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(hourly_trend.index, hourly_trend.values, marker='o', linestyle='-')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
ax.set_title('Tren Penyewaan Sepeda Berdasarkan Jam')
ax.set_xticks(range(24))
ax.grid(True)
st.pyplot(fig)

# Visualisasi Korelasi Cuaca dan Penyewaan Sepeda
st.subheader('Weather vs Bike Rental Correlation')
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(day_df[['temp', 'hum', 'windspeed', 'cnt']].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
ax.set_title("Korelasi antara Cuaca dan Penyewaan Sepeda")
st.pyplot(fig)

# Menampilkan statistik deskriptif dari data yang difilter
st.subheader('Descriptive Statistics of Filtered Data')
st.write(season_data.describe())
