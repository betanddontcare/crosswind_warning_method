from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def get_params():
    request_data = request.get_json()
    
    
@app.route('/get_para')
def show():
    return jsonify({'data' : para}) 

app.run(port=8000)