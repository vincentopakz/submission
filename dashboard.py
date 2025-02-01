import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
day_df = pd.read_csv('day.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim:", ["All"] + list(day_df['season'].unique()))
selected_weathersit = st.sidebar.selectbox("Pilih Cuaca:", ["All"] + list(day_df['weathersit'].unique()))

# Apply Filters
filtered_df = day_df.copy()
if selected_season != "All":
    filtered_df = filtered_df[filtered_df['season'] == selected_season]
if selected_weathersit != "All":
    filtered_df = filtered_df[filtered_df['weathersit'] == selected_weathersit]

st.title("Dashboard Analisis Penyewaan Sepeda")

# Visualisasi: Pengaruh Cuaca terhadap Penyewaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.boxplot(x=filtered_df['weathersit'], y=filtered_df['cnt'], ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# Visualisasi: Tren Penyewaan Sepeda Berdasarkan Hari dalam Seminggu
st.subheader("Tren Penyewaan Sepeda Berdasarkan Hari")
filtered_df['day_of_week'] = filtered_df['dteday'].dt.day_name()
rentals_by_day = filtered_df.groupby('day_of_week')['cnt'].mean().sort_values()
fig, ax = plt.subplots()
sns.barplot(x=rentals_by_day.index, y=rentals_by_day, ax=ax)
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
st.pyplot(fig)

st.write("**Kesimpulan:**")
st.write("- Penyewaan sepeda lebih tinggi saat cuaca cerah dan menurun saat cuaca buruk.")
st.write("- Jumlah penyewaan lebih tinggi pada hari kerja dibanding akhir pekan.")
