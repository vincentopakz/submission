import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan
sns.set(style="whitegrid")

# Load Data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Ubah format tanggal
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Judul Aplikasi
st.title("Dashboard Analisis Data - Bike Sharing")
st.markdown("**Menganalisis Tren dan Faktor yang Mempengaruhi Penyewaan Sepeda**")

# Sidebar untuk navigasi
menu = st.sidebar.radio("Pilih Visualisasi:", ["Tren Penyewaan Sepeda", "Pengaruh Cuaca terhadap Penyewaan"])

if menu == "Tren Penyewaan Sepeda":
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
    hourly_trend = hour_df.groupby('hr')['cnt'].mean()
    plt.figure(figsize=(10,5))
    plt.plot(hourly_trend.index, hourly_trend.values, marker='o', linestyle='-')
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Rata-rata Jumlah Penyewaan')
    plt.title('Tren Penyewaan Sepeda Berdasarkan Jam')
    plt.xticks(range(24))
    plt.grid(True)
    st.pyplot()
    st.markdown("**Insight:** Penyewaan sepeda meningkat pada jam sibuk pagi dan sore hari, sesuai dengan jam berangkat dan pulang kerja.")

elif menu == "Pengaruh Cuaca terhadap Penyewaan":
    st.subheader("Korelasi antara Cuaca dan Penyewaan Sepeda")
    plt.figure(figsize=(8,6))
    sns.heatmap(day_df[['temp', 'hum', 'windspeed', 'cnt']].corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Korelasi antara Cuaca dan Penyewaan Sepeda")
    st.pyplot()
    st.markdown("**Insight:** Temperatur memiliki korelasi positif dengan jumlah penyewaan sepeda, sementara kelembaban memiliki korelasi negatif yang lemah.")
