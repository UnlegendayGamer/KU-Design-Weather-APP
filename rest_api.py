from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the weather data into a pandas DataFrame
df = pd.read_csv('weatherdata.csv')

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
    global df  
    new_data = request.get_json()
    required_fields = ['date', 'weather_code', 'temperature_2m_max', 'temperature_2m_min', 'precipitation_sum', 'wind_speed_max', 'precipitation_probability_max']

    if all(field in new_data for field in required_fields):
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('weatherdata.csv', index=False)  # Save changes back to CSV
        return jsonify({'message': 'Data added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid request body'}), 400

# PUT request to edit data details
@app.route('/weather', methods=['PUT'])
def edit_weather_data():
    global df 
    date = request.args.get('date')
    data_point = request.args.get('data_point')
    value = request.args.get('value')

    if date and data_point and value and data_point in df.columns:
        df.loc[df['date'] == date, data_point] = value
        df.to_csv('weatherdata.csv', index=False)  
        return jsonify({'message': 'Data updated successfully'}), 200
    else:
        return jsonify({'error': 'Invalid request parameters'}), 400

@app.route('/weather', methods=['DELETE'])
def delete_weather_data():
    global df  
    date = request.args.get('date')

    if date:
        df = df[df['date'] != date]
        df.to_csv('weatherdata.csv', index=False) 
        return jsonify({'message': 'Data deleted successfully'}), 200
    else:
        return jsonify({'error': 'Invalid request parameters'}), 400

if __name__ == '__main__':
    app.run(debug=True)