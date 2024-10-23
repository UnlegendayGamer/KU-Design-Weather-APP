from flask import Flask, jsonify, request

app = Flask(__name__)
weather_data = {}

@app.route('/weather', methods=['GET'])
def get_weather_data():
    date = request.args.get('date')
    data_point = request.args.get('data_point')

    if date:
        if data_point:
            if date in weather_data and data_point in weather_data[date]:
                return jsonify({data_point: weather_data[date][data_point]}), 200
            return jsonify({"error": "Data point not found."}), 404
        return jsonify({date: weather_data.get(date, "No data found for this date.")}), 200
    return jsonify(weather_data), 200

@app.route('/weather', methods=['POST'])
def add_weather_data():
    data = request.json
    date = data.get('date')
    if not date or date in weather_data:
        return jsonify({"error": "Invalid date or data for this date already exists."}), 400

    weather_data[date] = {key: value for key, value in data.items() if key != 'date'}
    return jsonify({"message": "Data added.", "date": date, "data": weather_data[date]}), 201

@app.route('/weather/<date>', methods=['PUT'])
def edit_weather_data(date):
    if date not in weather_data:
        return jsonify({"error": "Date not found."}), 404

    data_point = request.json.get('data_point')
    value = request.json.get('value')

    if data_point in weather_data[date]:
        weather_data[date][data_point] = value
        return jsonify({"message": "Data updated.", "date": date, "data_point": data_point, "new_value": value}), 200
    return jsonify({"error": "Data point not found."}), 404

@app.route('/weather/<date>', methods=['DELETE'])
def delete_weather_data(date):
    if date in weather_data:
        del weather_data[date]
        return jsonify({"message": "Data deleted.", "date": date}), 200
    return jsonify({"error": "No data found for this date."}), 404

if __name__ == '__main__':
    app.run(debug=True)