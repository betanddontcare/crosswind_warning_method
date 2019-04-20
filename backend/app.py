from flask import Flask, jsonify, request
from flask_cors import CORS
from crosswind_warning_method import *

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def get_params():
    request_data = request.get_json()
    ratio = compute(request_data)
    return jsonify({'result' : ratio})

app.run(port=8000)