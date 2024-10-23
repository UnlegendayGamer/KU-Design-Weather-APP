from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from openmeteo_requests import Client
import requests_cache
from retry_requests import retry
from pydantic import BaseModel

app = FastAPI()

# Function to get weather data from Open-Meteo
def get_weather_info(latitude=52.52, longitude=13.41):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max", "precipitation_probability_max"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch"
    }
    responses = openmeteo.weather_api(url, params=params)
    
    if not responses:
        raise HTTPException(status_code=404, detail="No weather data available for the location")

    # Process the first location. You can modify for multiple locations.
    response = responses[0]

    # Extracting daily weather data
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(5).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "weather_code": daily_weather_code,
        "temperature_max": daily_temperature_2m_max,
        "temperature_min": daily_temperature_2m_min,
        "precipitation_sum": daily_precipitation_sum,
        "wind_speed_max": daily_wind_speed_10m_max,
        "precipitation_probability_max": daily_precipitation_probability_max,
    }

    # Convert the data into a pandas DataFrame
    daily_dataframe = pd.DataFrame(data=daily_data)
    
    return daily_dataframe

# FastAPI endpoint to get weather data
@app.get("/weather/")
async def get_weather(latitude: float = 52.52, longitude: float = 13.41):
    try:
        weather_df = get_weather_info(latitude, longitude)
        return weather_df.to_dict(orient="records")
    except Exception as e:
        return None

class WeatherData(BaseModel):
    date: str
    weather_code: int
    temperature_max: float
    temperature_min: float
    precipitation_sum: float
    wind_speed_max: float
    precipitation_probability_max: float

@app.post("/post_weather/")
async def post_weather(data: WeatherData):
    date = data.date
    weather_code = data.weather_code
    temperature_max = data.temperature_max
    temperature_min = data.temperature_min
    precipitation_sum = data.precipitation_sum
    wind_speed_max = data.wind_speed_max
    precipitation_probability_max = data.precipitation_probability_max

    # Define the data list
    data_list = [date, weather_code, temperature_max, temperature_min, precipitation_sum, wind_speed_max, precipitation_probability_max]

    # Open the weatherdata.txt file in read mode
    with open("weatherdata.txt", "r") as f:
        # Read all lines from the file
        lines = f.readlines()

    # Open the weatherdata.txt file in write mode
    with open("weatherdata.txt", "w") as f:
        # Append the data to each line of the file
        for i, line in enumerate(lines):
            if i < len(data_list):
                f.write(line.strip() + " " + str(data_list[i]) + "\n")
            else:
                f.write(line)
    return {"message": f"Weather data saved successfully {data}"}

@app.delete("/delete_weather/{date}")
async def delete_weather(date: str):
    lines = None
    with open("weatherdata.txt", 'r') as file:
        lines = file.readlines()

    date_array = lines[0].strip().split()
    weather_code_array = lines[1].strip().split()
    temperature_max_array = lines[2].strip().split()
    temperature_min_array = lines[3].strip().split()
    precipitation_sum_array = lines[4].strip().split()
    wind_speed_max_array = lines[5].strip().split()
    precipitaltion_probability_max_array = lines[6].strip().split()

    index = date_array.index(date)

    date_array[index] = ""
    weather_code_array[index] = ""
    temperature_max_array[index] = ""
    temperature_min_array[index] = ""
    precipitation_sum_array[index] = ""
    wind_speed_max_array[index] = ""
    precipitaltion_probability_max_array[index] = ""

    print(date_array)
    # Prepare the updated lines
    updated_lines = [
       ' '.join(date_array) + "\n",
       ' '.join(weather_code_array) + "\n",
       ' '.join(temperature_max_array) + "\n",
       ' '.join(temperature_min_array) + "\n",
       ' '.join(precipitation_sum_array) + "\n",
       ' '.join(wind_speed_max_array) + "\n",
       ' '.join(precipitaltion_probability_max_array) + "\n"
       ]

    file.close()

    # Write the updated data back to the file
    with open("weatherdata.txt", 'w') as file:
        file.writelines(updated_lines)
    return {"message": date}
