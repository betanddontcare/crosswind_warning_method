from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = []

@app.route('/', methods=['POST'])
def get_params():
    request_data = request.get_json()
    params = {
        'start' : request_data['start'],
        'stop' : request_data['stop'],
        'max_velocity' : request_data['max_velocity'],
        'front_area' : request_data['front_area'],
        'distance_axles' : request_data['distance_axles'],
        'front_axle_load' : request_data['front_axle_load'],
        'weight' : request_data['weight'],
        'wheel_radius' : request_data['wheel_radius'],
        'altitude' : request_data['altitude'],
        'rear_axle_load' : request_data['rear_axle_load']
    }
    data.append(params) 
    return jsonify(params) 

@app.route('/get_para')
def show():
    return jsonify({'data' : data}) 

app.run(port=8000)