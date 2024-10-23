# from fastapi import FastAPI
# import pandas as pd
# import os

# app = FastAPI()

# # Define the path where the CSV will be saved
# weather_data_path = "weatherdata.csv"

# # Helper function to load CSV data
# def load_weather_data():
#     if os.path.exists(weather_data_path):
#         return pd.read_csv(weather_data_path)
#     else:
#         return pd.DataFrame(columns=["date", "weather_code", "temperature_max", "temperature_min", "precipitation_sum", "wind_speed_max", "precipitation_probability_max"])

# # Helper function to save CSV data
# def save_weather_data(df):
#     df.to_csv(weather_data_path, index=False)

# @app.get("/weather/{date}")
# def get_weather_data(date: str):
#     df = load_weather_data()
#     result = df[df['date'] == date]
#     if result.empty:
#         return {"message": "No data available for this date"}
#     else:
#         return result.to_dict(orient="records")

# @app.post("/weather/")
# def add_weather_data(weather: dict):
#     df = load_weather_data()
#     new_data = pd.DataFrame([weather])
#     df = pd.concat([df, new_data], ignore_index=True)
#     save_weather_data(df)
#     return {"message": "Weather data added successfully"}

# @app.put("/weather/{date}")
# def update_weather_data(date: str, field: str, value: float):
#     df = load_weather_data()
#     if date in df['date'].values:
#         df.loc[df['date'] == date, field] = value
#         save_weather_data(df)
#         return {"message": f"Weather data for {date} updated successfully"}
#     else:
#         return {"message": f"No weather data found for date {date}"}
