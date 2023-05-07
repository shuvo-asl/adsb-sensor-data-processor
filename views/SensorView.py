import datetime
from flask_restful import Resource
import requests
from models.Position import Position
from models.PositionHistory import PositionHistory
class SensorView(Resource):
    def get(self):
        unique_data = []
        return {
            "status": "success",
            "data": unique_data
        }
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
                    position.speed = item['spd']
                    position.updated_at = datetime.datetime.utcnow()
                else:
                    position = Position(**{
                        "unique_code": hex_value,
                        "lat": item['lat'],
                        "lon": item['lon'],
                        "alt": item['alt'],
                        "speed": item['spd']
                    });

                position.save();

                if(item['lat'] is not None and item['lon'] is not None):
                    history = PositionHistory(**{
                        "unique_code": hex_value,
                        "lat":item['lat'],
                        "lon":item['lon'],
                        "location": "POINT({} {})".format(item['lat'],item['lon'])
                    })
                    history.save()
                hex_set.add(hex_value)
                unique_data.append(item)
        return {
            "status": "success",
            "data": unique_data
        }