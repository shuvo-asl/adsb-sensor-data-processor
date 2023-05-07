from flask_restful import Resource
from models.AircraftType import AircraftType
class Welcome(Resource):
    def get(self):
        return "ADSB Flight Data Processor is running...";

class Rnd(Resource):
    def get(self):
        locations = AircraftType.getAllAircraftType();
        data = [item.json() for item in locations]
        return {
            "data":data
        }