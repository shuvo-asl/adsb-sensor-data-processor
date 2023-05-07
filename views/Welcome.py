from flask_restful import Resource
from models.FlightPosition import FlightPosition
class Welcome(Resource):
    def get(self):
        return "ADSB Flight Data Processor is running...";

class Rnd(Resource):
    def get(self):
        locations = FlightPosition.getAllPositions();
        data = [item.json() for item in locations]
        return {
            "data":data
        }