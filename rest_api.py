from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the weather data into a pandas DataFrame
df = pd.read_csv('weather_data.csv')

# GET request to view given weather data as a function of data point(s) and timeframe
@app.route('/weather', methods=['GET'])
def get_weather_data():
    data_points = request.args.get('data_points')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if data_points and start_date and end_date:
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        filtered_df = filtered_df[data_points.split(',')]
        return jsonify(filtered_df.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Invalid request parameters'}), 400

# POST request to add new dates of data
@app.route('/weather', methods=['POST'])
def add_weather_data():
    new_data = request.get_json()
    if 'date' in new_data and 'weather_code' in new_data and 'temperature_2m_max' in new_data and 'temperature_2m_min' in new_data and 'precipitation_sum' in new_data and 'wind_speed_max' in new_data and 'precipitation_probability_max' in new_data:
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        return jsonify({'message': 'Data added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid request body'}), 400

# PUT request to edit data details
@app.route('/weather', methods=['PUT'])
def edit_weather_data():
    date = request.args.get('date')
    data_point = request.args.get('data_point')
    value = request.args.get('value')

    if date and data_point and value:
        df.loc[df['date'] == date, data_point] = value
        return jsonify({'message': 'Data updated successfully'}), 200
    else:
        return jsonify({'error': 'Invalid request parameters'}), 400

# DELETE request to remove specified dates (and their associated data points) from the stored data
@app.route('/weather', methods=['DELETE'])
def delete_weather_data():
    date = request.args.get('date')

    if date:
        df = df[df['date'] != date]
        return jsonify({'message': 'Data deleted successfully'}), 200
    else:
        return jsonify({'error': 'Invalid request parameters'}), 400

if __name__ == '__main__':
    app.run(debug=True)