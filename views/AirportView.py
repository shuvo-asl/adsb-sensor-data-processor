from flask_restful import Resource
from models.Airport import Airport
from flask import jsonify
class AirportView(Resource):
    def get(self,iso_code="BD"):
        # get all airport from the db by ISO code and return to the response
        airports = Airport.getAllAirportsByIsoCode(iso_code)
        return {
            "status":True,
            "data":airports
        }