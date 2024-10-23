import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import sys

try:
    dataframe = None

    # File upload functionality
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        new_file = uploaded_file.getvalue().decode("utf-8")
        temp_val = new_file.replace(": ", ",").replace(" ", ",")
        
        with open("weatherdata.csv", "w") as f:
            f.write(temp_val)
        
        with open("weatherdata.csv", "r") as r, open("weatherdata2.csv", "w") as w:
            for line in r:
                if line.strip():
                    w.write(line)
        
        dataframe = pd.read_csv("weatherdata2.csv")

        # Flip the dataframe for better display
        flipped_df = dataframe.T
        flipped_df.columns = flipped_df.iloc[0]
        flipped_df = flipped_df.iloc[1:]
        flipped_df = flipped_df.reset_index()
        st.dataframe(flipped_df)

        # Select box for choosing data type to compare
        option = st.selectbox(
            "What data would you like to compare?",
            ("weather_code", "temperature_max", "temperature_min", "precipitation_sum", "wind_speed_max", "precipitation_probability_max")
        )
        st.bar_chart(data=flipped_df, x="index", y=option, color="#40242c")

    # Latitude and Longitude input for API request
    latitude = st.number_input("Latitude", value=52.52)
    longitude = st.number_input("Longitude", value=13.41)

    # Request weather data from FastAPI backend
    if st.button("Get Weather Data"):
        try:
            # Call FastAPI endpoint to get weather data from Open-Meteo API
            response = requests.get(f"http://127.0.0.1:8000/weather/?latitude={latitude}&longitude={longitude}")
            
            if response.status_code == 200:
                api_data = response.json()
                api_df = pd.DataFrame(api_data)
                api_data['date'] = api_df["date"].replace('T00:00:00+00:00', '')
                st.dataframe(api_df)
            else:
                st.error("Failed to fetch data from the API.")
                
            api_df['date'] = api_df['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(api_df)

            user_choice = st.selectbox(
                "What data would you like to compare?",
                ("weather_code", "temperature_max", "temperature_min", "precipitation_sum", "wind_speed_max", "precipitation_probability_max"), key="1"
            )
            
            date_slider = st.select_slider(
                "Select a date range",
                options=api_df['date'],
                value=(api_df['date'].min(), api_df['date'].max())
            )
            
            # filter the data to the selected date range
            filtered_df = api_df[(api_df['date'] >= date_slider[0]) & (api_df['date'] <= date_slider[1])]

            st.bar_chart(filtered_df[['date', user_choice]].set_index('date'), color="#40242c")

            if (filtered_df[user_choice].max() > flipped_df[user_choice].max()):
                max_value = filtered_df[user_choice].max()
            else:
                max_value = flipped_df[user_choice].max()
            st.write("In the given data, the " + user_choice + " was " + str(flipped_df[user_choice].max()) + ", while the " + user_choice + " at latitude " + str(latitude) + " longitude " + str(longitude) + ", was " + str(max_value))
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}", file=sys.stderr)
    st.error(f"An error occurred: {str(e)}")