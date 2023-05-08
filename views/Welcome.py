from flask_restful import Resource
from models.Flight import Flight
class Welcome(Resource):
    def get(self):
        return "ADSB Flight Data Processor is running...";

class Rnd(Resource):
    def get(self):
        locations = Flight.getAllFlights();
        data = [item.json() for item in locations]
        return {
            "data":data
        }