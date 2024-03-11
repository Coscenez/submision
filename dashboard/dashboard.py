import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
df = pd.read_csv("day.csv")

# Data preprocessing
column_mapping = {'dteday': 'date', 'yr': 'year', 'mnth': 'month', 'temp': 'temperature', 'hum': 'humidity','cnt': 'total'}
df.rename(columns=column_mapping, inplace=True)
df.drop_duplicates(inplace=True)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Calculate outliers and remove them
Q1 = df.select_dtypes(include=np.number).quantile(0.25)
Q3 = df.select_dtypes(include=np.number).quantile(0.75)
IQR = Q3 - Q1
outliers = ((df.select_dtypes(include=np.number) < (Q1 - 1.5 * IQR)) | (df.select_dtypes(include=np.number) > (Q3 + 1.5 * IQR))).any(axis=1)
df = df[~outliers]

# Convert day_of_week to categorical for proper sorting
df['day_of_week'] = df['date'].dt.day_name()
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=days_order, ordered=True)

# Conclusion
conclusion_text = """
Berdasarkan analisis yang dilakukan, dapat disimpulkan bahwa temperatur memiliki pengaruh yang signifikan terhadap jumlah peminjaman sepeda, dengan semakin tingginya suhu menyebabkan peningkatan jumlah peminjaman. Namun, kelembaban dan kecepatan angin tidak terlalu berpengaruh. Selain itu, pola mingguan juga memengaruhi jumlah peminjaman sepeda, dimana jumlahnya cenderung lebih tinggi pada hari-hari kerja dibandingkan dengan akhir pekan, dengan puncak peminjaman pada hari Kamis dan Jumat, dan penurunan pada Sabtu dan Minggu.
"""

# Sidebar
st.sidebar.title('Bike Rental Analysis Dashboard')
plot_type = st.sidebar.selectbox('Select Plot Type', ['Histogram', 'Scatter Plot (Temperature vs Total)', 'Scatter Plot (Humidity vs Total)', 'Scatter Plot (Windspeed vs Total)', 'Average Rental per Day of Week', 'Conclusion'])

# Main content
st.title('Bike Rental Analysis Dashboard')

# Define fig variable outside the if-elif blocks
fig, ax = plt.subplots()

if plot_type == 'Histogram':
    st.subheader('Distribution of Total Bike Rentals')
    ax.hist(df['total'], bins=20)
    ax.set_xlabel('Count')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Count')
    st.pyplot(fig)

elif plot_type == 'Scatter Plot (Temperature vs Total)':
    st.subheader('Relationship between Temperature and Total Bike Rentals')
    sns.scatterplot(data=df, x='temperature', y='total', ax=ax)
    ax.set_title('Relationship between Temperature and Total Bike Rentals')
    ax.set_xlabel('Temperature (C)')
    ax.set_ylabel('Total Bike Rentals')
    st.pyplot(fig)

elif plot_type == 'Scatter Plot (Humidity vs Total)':
    st.subheader('Relationship between Humidity and Total Bike Rentals')
    sns.scatterplot(data=df, x='humidity', y='total', ax=ax)
    ax.set_title('Relationship between Humidity and Total Bike Rentals')
    ax.set_xlabel('Humidity (%)')
    ax.set_ylabel('Total Bike Rentals')
    st.pyplot(fig)

elif plot_type == 'Scatter Plot (Windspeed vs Total)':
    st.subheader('Relationship between Windspeed and Total Bike Rentals')
    sns.scatterplot(data=df, x='windspeed', y='total', ax=ax)
    ax.set_title('Relationship between Windspeed and Total Bike Rentals')
    ax.set_xlabel('Windspeed (km/h)')
    ax.set_ylabel('Total Bike Rentals')
    st.pyplot(fig)

elif plot_type == 'Average Rental per Day of Week':
    st.subheader('Average Rental per Day of Week')
    daily_avg = df.groupby('day_of_week')['total'].mean().reset_index()
    sns.barplot(data=daily_avg, x='day_of_week', y='total', palette='viridis', ax=ax)
    ax.set_title('Average Rental per Day of Week')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Average Rental Count')
    st.pyplot(fig)

elif plot_type == 'Conclusion':
    st.subheader('Conclusion')
    st.write(conclusion_text)

