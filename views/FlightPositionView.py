from flask_restful import Resource
import requests
from models.FlightPosition import FlightPosition
class FlightPositionView(Resource):
    def get(self,flight_no):
        data = []
        if flight_no is None:
            return {
                "status" : "Failed",
                "msg":"Unknown Request"
            },404

        histories = FlightPosition.getAllPositionHistoryByFlightNo(flight_no)
        if histories is not None:
            data = [item.json() for item in histories]


        return {
            "status":"success",
            "data":data
        },200

