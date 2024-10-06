import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style untuk seaborn
sns.set(style='dark')

st.header('Bike Rentals :sparkles:')

# Membaca data
all_df = pd.read_csv("all_data.csv")

# Pastikan kolom dteday ada dalam format datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

def create_daily_rentals_df(all_df):
    # Menghitung total penyewaan per hari
    daily_rentals_df = all_df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)
    
    return daily_rentals_df

# Membuat daily_rentals_df
daily_rentals_df = create_daily_rentals_df(all_df)

# Sekarang Anda bisa menggunakan daily_rentals_df dalam Streamlit
st.subheader('Daily Bike Rentals')

# Total penyewaan sepeda
total_rentals = daily_rentals_df.total_rentals.sum()  
st.metric("Total Rentals", value=total_rentals)


"""
## Menghitung rerata penyewaan per season
"""

# Grouping berdasarkan season dan menghitung sum dari 'cnt' untuk setiap musim
byseason_df = all_df.groupby(by="season").cnt.mean().reset_index()

# Ubah angka season menjadi nama musim
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
byseason_df['season'] = byseason_df['season'].map(season_mapping)

# Ubah season menjadi string untuk keperluan visualisasi
byseason_df['season'] = byseason_df['season'].astype(str)
byseason_df.rename(columns={
    "cnt": "total_rentals"
}, inplace=True)


# Membuat objek Figure dan Axes
fig, ax = plt.subplots(figsize=(10, 5))

# Pastikan jumlah kategori sesuai dengan warna
unique_seasons = byseason_df['season'].nunique()  # Menghitung jumlah kategori unik
colors = sns.color_palette("husl", unique_seasons)  # Mendapatkan palette yang sesuai

# Membuat bar plot untuk total rentals berdasarkan musim
sns.barplot(
    x="total_rentals",
    y="season",
    data=byseason_df.sort_values(by="total_rentals", ascending=False),
    palette=colors,
    ax=ax
)

# Set judul dan label
ax.set_title("Rerata Penyewaan Sepeda Berdasarkan Musim", fontsize=15)
ax.set_ylabel("Musim", fontsize=12)
ax.set_xlabel("Rerata Penyewaan Sepeda", fontsize=12)
plt.tick_params(axis='y', labelsize=12)

# Tampilkan grafik di Streamlit
st.pyplot(fig)
"""
## Menghitung rerata penyewaan sepeda berdasarkan holiday dan workingday 

"""
byday_df = all_df.groupby(by=["holiday", "workingday"]).cnt.mean().reset_index()

byday_df.rename(columns={
    "cnt": "total_rentals"
}, inplace=True)

byday_df['holiday'] = byday_df['holiday'].replace({0: 'Workingday', 1: 'Holiday'})

# Membuat objek Figure dan Axes
fig, ax = plt.subplots(figsize=(10, 5))

# Pastikan jumlah kategori sesuai dengan warna
unique_day = byday_df['holiday'].nunique()  # Menghitung jumlah kategori unik
colors = sns.color_palette("husl", unique_day)  # Mendapatkan palette yang sesuai

# Membuat bar plot untuk total rentals berdasarkan musim
sns.barplot(
    x="total_rentals",
    y="holiday",
    hue="workingday",
    data=byday_df.sort_values(by="total_rentals", ascending=False),
    palette=colors,
    ax=ax
)
# Set judul dan label
ax.set_title("Rerata Penyewaan Sepeda Berdasarkan Holiday dan Workingday", fontsize=15)
ax.set_ylabel("Holiday Status", fontsize=12)
ax.set_xlabel("Rerata Penyewaan Sepeda", fontsize=12)
plt.tick_params(axis='y', labelsize=12)

# Tampilkan grafik di Streamlit
st.pyplot(fig)