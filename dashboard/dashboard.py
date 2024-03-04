import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "casual": "rent_count",
        "registered": "register",
        "cnt": "revenue"
    }, inplace=True)

    return daily_orders_df


def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='M', on='dteday').agg({
        "mnth": "unique",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "mnth": "month",
        "casual": "rent_count",
        "registered": "register",
        "cnt": "revenue"
    }, inplace=True)

    return monthly_orders_df


def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "revenue"
    }, inplace=True)

    return byseason_df


# Load cleaned data
all_df = pd.read_csv("https://raw.githubusercontent.com/dMorran/Submiss/main/dashboard/main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) &
                 (all_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
daily_orders_df = create_daily_orders_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)
byseason_df = create_byseason_df(main_df)

st.subheader('Daily Rent')

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = daily_orders_df.rent_count.sum()
    st.metric("Total Casual Rents", value=total_orders)

with col2:
    total_revenue = daily_orders_df.register.sum()
    st.metric("Total Register Rent", value=total_revenue)

with col3:
    total_revenue = daily_orders_df.revenue.sum()
    st.metric("Total Rent", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["rent_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader('Monthly Rent')

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = monthly_orders_df.rent_count.sum()
    st.metric("Total Casual Rents", value=total_orders)

with col2:
    total_revenue = monthly_orders_df.register.sum()
    st.metric("Total Register Rent", value=total_revenue)

with col3:
    total_revenue = monthly_orders_df.revenue.sum()
    st.metric("Total Rent", value=total_revenue)

# Create a dictionary to map month numbers to month names
month_names = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

# Map the month numbers to month names
monthly_orders_df["month_name"] = monthly_orders_df["dteday"].dt.month.map(
    month_names)

# Create a bar plot with month names on the x-axis
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    monthly_orders_df["month_name"],
    monthly_orders_df["rent_count"],
    color="#90CAF9"
)
ax.set_ylabel("Rental Count", fontsize=20)
ax.set_xlabel("Month", fontsize=20)
ax.tick_params(axis='both', labelsize=15)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

st.pyplot(fig)

st.subheader('Season Rent')


# Mengganti format angka musim menjadi nama musim
season_titles = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
byseason_df['season'] = byseason_df['season'].map(season_titles)

# Membuat grafik batang
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season", y="revenue", data=byseason_df, palette="muted", ax=ax)
ax.set_title("Total Revenue by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Total Revenue")
st.pyplot(fig)
