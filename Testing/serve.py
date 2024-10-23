def update_weather_data(filename, date_to_update, data_point, new_value):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Helper function to safely split lines into key-value pairs
    def split_line(line):
        parts = line.strip().split(": ")
        if len(parts) == 2:
            return parts[1].split()  # use split() without arguments to handle extra spaces
        else:
            return []  # Return empty if the format isn't correct

    # Split each line safely
    data = {
        'date': split_line(lines[0]),
        'weather_code': split_line(lines[1]),
        'temperature_max': split_line(lines[2]),
        'temperature_min': split_line(lines[3]),
        'precipitation_sum': split_line(lines[4]),
        'wind_speed_max': split_line(lines[5]),
        'precipitation_probability_max': split_line(lines[6])
    }

    # Remove any extra spaces or line breaks from the date
    date_to_update = date_to_update.strip()

    # Check if the date exists in the data
    if date_to_update not in data['date']:
        print(f"Date {date_to_update} not found.")
        return

    # Find the index of the date
    index_to_update = data['date'].index(date_to_update)

    # Check if the data_point exists in the dictionary
    if data_point not in data:
        print(f"Data point {data_point} not found.")
        return

    # Update the value in the respective data array
    data[data_point][index_to_update] = str(new_value)

    # Prepare the updated lines for writing back to the file
    updated_lines = [
        f"date: {' '.join(data['date'])}\n",
        f"weather_code: {' '.join(data['weather_code'])}\n",
        f"temperature_max: {' '.join(data['temperature_max'])}\n",
        f"temperature_min: {' '.join(data['temperature_min'])}\n",
        f"precipitation_sum: {' '.join(data['precipitation_sum'])}\n",
        f"wind_speed_max: {' '.join(data['wind_speed_max'])}\n",
        f"precipitation_probability_max: {' '.join(data['precipitation_probability_max'])}\n"
    ]

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        file.writelines(updated_lines)

    print(f"Updated {data_point} for date {date_to_update} to {new_value}.")


update_weather_data('weatherdata.txt', '2024-04-26', 'temperature_max', 65.0)