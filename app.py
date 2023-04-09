from flask import Flask,jsonify
from flask_cors import CORS
import requests
app = Flask(__name__)
cors = CORS(app)
@app.route("/")
def getData():
    khulna = requests.get("http://192.168.201.3/aircraftlist.json").json();
    dhaka = requests.get("http://192.168.30.27/aircraftlist.json").json();

    # Combine the JSON objects into a single list
    data_list = []
    data_list.extend(khulna)
    data_list.extend(dhaka)
    unique_data = []
    hex_set = set()

    for item in data_list:
        hex_value = item['hex']
        if hex_value not in hex_set:
            hex_set.add(hex_value)
            unique_data.append(item)
    return {
        "status":"success",
        "data":unique_data
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)