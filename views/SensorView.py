from flask_restful import Resource
import requests
from models.Position import Position
class SensorView(Resource):
    def get(self):
        unique_data = []
        khulna = requests.get("http://192.168.201.3/aircraftlist.json").json();
        dhaka = requests.get("http://192.168.30.27/aircraftlist.json").json();

        # Combine the JSON objects into a single list
        data_list = []
        data_list.extend(khulna)
        data_list.extend(dhaka)
        hex_set = set()

        for item in data_list:
            hex_value = item['hex']
            if hex_value not in hex_set:
                position = Position.getPositionByUniqueCode(hex_value);
                if position:
                    position.lat = item['lat']
                    position.lon = item['lon']
                    position.alt = item['alt']
                else:
                    position = Position(**{
                        "unique_code": hex_value,
                        "lat": item['lat'],
                        "lon": item['lon'],
                        "alt": item['alt']
                    });

                position.save();
                hex_set.add(hex_value)
                unique_data.append(item)
        return {
            "status": "success",
            "data": unique_data
        }