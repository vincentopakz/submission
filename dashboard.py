import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Memuat dataset
day_df = pd.read_csv('day.csv')

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

# Filter berdasarkan cuaca
weather_filter = st.selectbox('Select Weather Situation', options=[1, 2, 3], format_func=lambda x: ['Clear', 'Mist', 'Heavy Rain'][x-1])

# Filter data berdasarkan cuaca
weather_data = season_data[season_data['weathersit'] == weather_filter]

# Menampilkan data yang difilter
st.write(f"Data dengan kondisi cuaca: {['Clear', 'Mist', 'Heavy Rain'][weather_filter - 1]}")
st.write(weather_data)

# Visualisasi data yang difilter
st.subheader('Visualization of Filtered Data')

# Membuat figure dan axis secara eksplisit
fig, ax = plt.subplots(figsize=(10, 6))

# Plot boxplot
sns.boxplot(x='season', y='cnt', data=weather_data, palette='Set2', ax=ax)
ax.set_title('Bike Sharing Count per Season (Filtered)')

# Menampilkan visualisasi
st.pyplot(fig)

# Menampilkan statistik deskriptif dari data yang difilter
st.subheader('Descriptive Statistics of Filtered Data')
st.write(weather_data.describe())
