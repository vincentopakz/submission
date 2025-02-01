import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar filters
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", day_df['dteday'].min())
end_date = st.sidebar.date_input("End Date", day_df['dteday'].max())
season_filter = st.sidebar.multiselect("Select Season", day_df['season'].unique(), day_df['season'].unique())
weather_filter = st.sidebar.multiselect("Select Weather", day_df['weathersit'].unique(), day_df['weathersit'].unique())

# Apply filters
filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
filtered_df = filtered_df[filtered_df['season'].isin(season_filter) & filtered_df['weathersit'].isin(weather_filter)]

# Dashboard Title
st.title("Rental Bike Analysis Dashboard")

# Visualization: Pengaruh Cuaca terhadap Penyewaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(x=filtered_df['weathersit'], y=filtered_df['cnt'], ax=ax)
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(fig)

# Visualization: Tren Penyewaan Sepeda Berdasarkan Hari
st.subheader("Tren Penyewaan Sepeda Berdasarkan Hari")
filtered_df['day_of_week'] = filtered_df['dteday'].dt.day_name()
rentals_by_day = filtered_df.groupby('day_of_week')['cnt'].mean().sort_values()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=rentals_by_day.index, y=rentals_by_day, ax=ax)
ax.set_xlabel('Hari dalam Seminggu')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
st.pyplot(fig)

# Show filtered dataset
st.subheader("Filtered Data Preview")
st.write(filtered_df.head())
