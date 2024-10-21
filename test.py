import streamlit as st
import pandas as pd
import numpy as np

# Sample weather data (in reality, load from a file)
weather_data = {
    'date': ['2024-04-24', '2024-04-25', '2024-04-26', '2024-04-27', '2024-04-28', '2024-04-29'],
    'weather_code': [3.0, 61.0, 3.0, 55.0, 3.0, 63.0],
    'temperature_max': [54.95, 52.61, 61.97, 52.25, 52.61, 48.47],
    'temperature_min': [44.24, 47.12, 48.65, 47.93, 42.80, 40.01],
    'precipitation_sum': [0.0, 0.22, 0.0, 0.15, 0.0, 0.30],
    'wind_speed_max': [9.31, 10.12, 8.25, 10.71, 13.59, 7.45]
}

# Convert data to DataFrame for easy manipulation
df = pd.DataFrame(weather_data)

# Streamlit app layout
st.title("Weather Data Query Application")
st.write("Interactively query weather data based on the input file.")

# Data points for querying
data_point = st.selectbox('Select Data Point', df.columns[1:])  # Exclude date from data points
query_type = st.selectbox('Select Query Type', ['max', 'min', 'average', 'single point'])

# Date range input
start_date, end_date = st.select_slider(
    'Select Date Range',
    options=df['date'],
    value=(df['date'].min(), df['date'].max())
)

# Function to calculate summary statistics
def get_weather_summary(query_type, data_point, start_date, end_date):
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    data = df.loc[mask, data_point]
    
    if query_type == 'max':
        return np.max(data)
    elif query_type == 'min':
        return np.min(data)
    elif query_type == 'average':
        return np.mean(data)
    elif query_type == 'single point':
        return data.iloc[0]  # Just for demo purposes

if st.button('Get Results'):
    result = get_weather_summary(query_type, data_point, start_date, end_date)
    st.write(f"Result: {result}")

if st.checkbox('Show Histogram'):
    st.bar_chart(df.set_index('date')[data_point])