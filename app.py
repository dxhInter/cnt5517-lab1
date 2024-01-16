import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import json
import os

app = Flask(__name__)

'''
this is a function that to show a json string from data.json file
'''
@app.route('/show_data')
def show_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data), 200
    return jsonify('No data available'), 400

'''
this is a function that to receive a json string from edge computer
in json string format
it's like the following:
{"temperatureAndHumidity": "25.7+53.0", "timestamp": "2024-01-15 16:45:10"}
'''
@app.route('/resv_dht_data', methods=['POST'])
def resv_dht_data():
    try:
        temp_and_humi = request.args['temperatureAndHumidity']
        formatted_datetime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        with open('data.json', 'w') as outfile:
            json.dump(
                {
                    'temperatureAndHumidity': temp_and_humi,
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
