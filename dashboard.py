import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Convert date column
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# Streamlit UI
st.title("📊 Dashboard Analisis Rental Sepeda")
st.write("Dashboard interaktif untuk melihat tren penyewaan sepeda berdasarkan musim dan hari.")

# Sidebar Filters
year_option = st.sidebar.selectbox("Pilih Tahun:", [2011, 2012])
filtered_df = day_df[day_df["yr"] == (year_option - 2011)]

# Rental Bike per Season
st.subheader("Rata-rata Penyewaan Sepeda per Musim")
season_counts = filtered_df.groupby("season")["cnt"].mean()
fig, ax = plt.subplots()
ax.bar(season_counts.index, season_counts, color=["blue", "green", "orange", "red"])
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
ax.set_ylabel("Rata-rata Jumlah Rental")
st.pyplot(fig)

# Rental Bike per Day
st.subheader("Rata-rata Penyewaan Sepeda per Hari")
filtered_df["day_of_week"] = filtered_df["dteday"].dt.day_name()
rentals_by_day = filtered_df.groupby("day_of_week")["cnt"].mean()
fig, ax = plt.subplots()
ax.bar(rentals_by_day.index, rentals_by_day, color="purple")
ax.set_ylabel("Rata-rata Jumlah Rental")
plt.xticks(rotation=45)
st.pyplot(fig)

st.write("📌 **Insight:** Musim Fall memiliki rata-rata rental tertinggi. Sedangkan hari Jumat cenderung memiliki jumlah rental tertinggi.")