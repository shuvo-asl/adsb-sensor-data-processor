from flask_restful import Resource
from models.FlightPosition import FlightPosition
from models.Flight import Flight
from models.Airport import Airport
class FlightPositionView(Resource):
    def get(self,flight_no):
        position_histories = []
        flight = Flight.getFlightByFlightNo(flight_no)

        if flight_no is None or flight is None:
            return {
                "status" : "Failed",
                "msg":"Unknown Request"
            },404
        flight = flight.json()
        flight['org_airport'] = Airport.getAirportByIcao(flight['src'])
        flight['dst_airport'] = Airport.getAirportByIcao(flight['destination'])

        histories = FlightPosition.getAllPositionHistoryByFlightNo(flight_no)
        if histories is not None:
            position_histories = [item.json() for item in histories]

        data = {
            "flight_information":flight,
            "position_histories":position_histories
        }
        return {
            "status":"success",
            "data":data
        },200

