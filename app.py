import datetime

from flask import Flask, jsonify, request
import time
import json
import os

app = Flask(__name__)

'''
this is a function that to show a json string from dht11_data.json file
'''
@app.route('/show_data', methods=['GET'])
def show_data():
    if os.path.exists('dht11_data.json'):
        with open('dht11_data.json', 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data), 200
    return jsonify('No data available'), 400

'''
this is a function that to receive a json string from edge computer
in json string format
it's like the following:
{"temperature": 25.4, "humidity": 55.0, "timestamp": "2024-01-15 17:10:18"}
'''
@app.route('/resv_dht_data', methods=['POST'])
def resv_dht_data():
    try:
        # temp_and_humi = request.args['temperatureAndHumidity']
        data = request.json
        temperature = data['temperature']
        humidity = data['humidity']
        formatted_datetime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        with open('dht11_data.json', 'w') as outfile:
            json.dump(
                {
                    'temperature': temperature,
                    'humidity': humidity,
                    'timestamp': formatted_datetime
                },
                outfile
            )

        return jsonify({
            'msg': 'Data added'
        }), 201
    except KeyError:
        return jsonify({'error': 'Missing temperature and humidity parameter'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
