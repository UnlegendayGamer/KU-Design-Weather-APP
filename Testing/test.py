import re

def split_dates(date_string):
    # Remove the 'date:' prefix
    date_string = date_string.replace('date:', '')
    
    # Use regex to find all the substrings that match the date format YYYY-MM-DD
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', date_string)
    
    return dates

def put_weather(date, data_point, value):
    with open("weatherdata.txt", 'r') as file:
        lines = file.readlines()

    date_array = lines[0].strip().split()
    weather_code_array = str(lines[1]).strip().split()
    temperature_max_array = str(lines[2]).strip().split()
    temperature_min_array = str(lines[3]).strip().split()
    precipitation_sum_array = str(lines[4]).strip().split()
    wind_speed_max_array = str(lines[5]).strip().split()
    precipitaltion_probability_max_array = str(lines[6]).strip().split()

    # print(split_dates(str(date_array)))
    
    date_array = split_dates(str(date_array))
    index = date_array.index(str(date))
        
    if data_point == "weather_code":
        weather_code_array[index] = value
    elif data_point == "temperature_max":
        temperature_max_array[index] = value
    elif data_point == "temperature_min":
        temperature_min_array[index] = value
    elif data_point == "precipitation_sum":
        precipitation_sum_array[index] = value
    elif data_point == "wind_speed_max":
        wind_speed_max_array[index] = value
    elif data_point == "precipitaltion_probability_max":
        precipitaltion_probability_max_array[index] = value
    
    print(temperature_min_array[index])

    updated_lines = [
        ' '.join(str(date_array)) + "\n",
        ' '.join(str(weather_code_array)) + "\n",
        ' '.join(str(temperature_max_array)) + "\n",
        ' '.join(str(temperature_min_array)) + "\n",
        ' '.join(str(precipitation_sum_array)) + "\n",
        ' '.join(str(wind_speed_max_array)) + "\n",
        ' '.join(str(precipitaltion_probability_max_array)) + "\n"
    ]
    
    print(updated_lines)

    file.close()

    # Write the updated data back to the file
    with open("weatherdata.txt", 'w') as file:
        file.writelines(updated_lines)

put_weather("2024-04-24", "temperature_min", 0.0)