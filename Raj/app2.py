import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from requests.structures import CaseInsensitiveDict

def post_weather(date, weather_code, temperature_max, temperature_min, precipitation_sum, wind_speed_max, precipitation_probability_max, token):
    url = "http://localhost:8000/post_weather/"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    headers["Content-Type"] = "application/json"

    data = f"""
    {{
      "date": "{date}",
      "weather_code": {weather_code},
      "temperature_max": {temperature_max},
      "temperature_min": {temperature_min},
      "precipitation_sum": {precipitation_sum},
      "wind_speed_max": {wind_speed_max},
      "precipitation_probability_max": {precipitation_probability_max}
    }}
    """

    resp = requests.post(url, headers=headers, data=data)
    return resp.status_code

dataframe = None
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    new_file = uploaded_file.getvalue().decode("utf-8")
    # st.write(new_file)
    temp_val = new_file.replace(": ", ",").replace(" ", ",")
    
    f = open("weatherdata.csv", "w")
    f.write(temp_val)
    f.close()
    
    with open("weatherdata.csv", "r") as r, open("weatherdata2.csv", "w") as w:
        for line in r:
            if line.strip():
                w.write(line)
    
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv("weatherdata2.csv")
    # st.dataframe(dataframe)
    
    flipped_df = dataframe.T
    flipped_df.columns = flipped_df.iloc[0]
    flipped_df = flipped_df.iloc[1:]
    flipped_df = flipped_df.reset_index()
    st.dataframe(flipped_df)

    option = st.selectbox(
        "What data would you like to compare?",
        ("weather_code", "temperature_max", "temperature_min", "precipitation_sum", "wind_speed_max", "precipitation_probability_max"),
    )

    st.bar_chart(data=flipped_df, x="index", y=option, color="#40242c", stack=False)
    
    df = None
    
    latitude = st.number_input("Latitude")
    longitude = st.number_input("Longitude")
    
    response = requests.get(f"http://127.0.0.1:8000/weather/?latitude={latitude}&longitude={longitude}")
    api_data = response.json()
    df = pd.DataFrame(api_data)
    df['date'] = df["date"].replace('T00:00:00+00:00', '')
    st.write("This is the generated timestamps: " + option)
    st.dataframe(df)

    user_choice = st.selectbox(
        "What data would you like to compare?",
        ("weather_code", "temperature_max", "temperature_min", "precipitation_sum", "wind_speed_max", "precipitation_probability_max"), key="1"
    )
    
    date_slider = st.select_slider(
        "Select a date range",
        options=df['date'],
        value=(df['date'].min(), df['date'].max())
    )
    
    # filter the data to the selected date range
    filtered_df = df[(df['date'] >= date_slider[0]) & (df['date'] <= date_slider[1])]

    st.bar_chart(filtered_df[['date', user_choice]].set_index('date'), color="#40242c")

    if (filtered_df[user_choice].max() > flipped_df[user_choice].max()):
        max_value = filtered_df[user_choice].max()
    else:
        max_value = flipped_df[user_choice].max()
    st.write("In the given data, the " + user_choice + " was " + str(flipped_df[user_choice].max()) + ", while the " + user_choice + " at latitude " + str(latitude) + " longitude " + str(longitude) + ", was " + str(max_value))
    
    date = st.text_input("Enter date (YYYY-MM-DD):")
    weather_code = st.text_input("Enter weather code:")
    temperature_max = st.text_input("Enter maximum temperature:")
    temperature_min = st.text_input("Enter minimum temperature:")
    precipitation_sum = st.text_input("Enter total precipitation:")
    wind_speed_max = st.text_input("Enter maximum wind speed:")
    precipitation_probability_max = st.text_input("Enter maximum probability of precipitation:")

    if st.button("Submit"):
        try:
            weather_code = int(weather_code)
            temperature_max = float(temperature_max)
            temperature_min = float(temperature_min)
            precipitation_sum = float(precipitation_sum)
            wind_speed_max = float(wind_speed_max)
            precipitation_probability_max = float(precipitation_probability_max)
        except ValueError:
            st.error("Invalid input. Please enter a valid number for weather code, temperature, precipitation, wind speed, and probability.")
        else:
            status_code = post_weather(date, weather_code, temperature_max, temperature_min, precipitation_sum, wind_speed_max, precipitation_probability_max, token="123")
            st.write(f"Status code: {status_code}")

    date_to_delete = st.text_input("Enter date (YYYY-MM-DD) to delete:", key="2")

    if st.button("Delete"):
        try:
            date_to_delete = str(date_to_delete)
        except KeyError:
            st.error("Invalid input. Please enter a valid date.")
        else:
            import httpx

            url = f"http://localhost:8000/delete_weather/{date_to_delete}/"

            response = httpx.delete(url)

            if response.status_code == 200:
                print("Weather data deleted successfully")
            else:
                print("Error:", response.text)
    
    