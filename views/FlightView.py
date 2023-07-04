from flask_restful import Resource
from models.Flight import Flight
"""
This class is responsible to manage Flight List data
"""
class FlightView(Resource):
    def get(self,flight_status=None):

        if flight_status is not None and flight_status not in ['pending','running','completed']:
            return {
                "status": "failed",
                "msg": "UnProcessable Request",
            }, 422

        if flight_status is not None:
            flights = Flight.getFlightByStatus(flight_status)
        else:
            flights = Flight.getAllFlights()

        if bool(flights) is False:
            return {
                "status": "success",
                "msg": "No Data Found.",
            }, 404

        flights = [flight.json() for flight in flights]
        return {
            "status":"success",
            "msg" : "Flight data is ready to deliver.",
            "data": flights
        },200