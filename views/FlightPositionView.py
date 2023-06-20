from flask_restful import Resource
from models.FlightPosition import FlightPosition
from models.Flight import Flight
from models.Airport import Airport
class FlightPositionView(Resource):
    # This method provide the single flight details with the flight no
    def get(self,flight_no):
        position_histories = [] #declare this array to store all of positional history

        # Get the flight details
        flight = Flight.getFlightByFlightNo(flight_no)

        # IF the flight is not found by the flight no then return response failed with code 404
        if flight_no is None or flight is None:
            return {
                "status" : "Failed",
                "msg":"Unknown Request"
            },404

        # convert flight class object to json
        flight = flight.json()

        #renaming the key of src and destination airport which is doing for frontend alignment
        flight['org_airport'] = Airport.getAirportByIcao(flight['src'])
        flight['dst_airport'] = Airport.getAirportByIcao(flight['destination'])

        # get All history by flight no
        histories = FlightPosition.getAllPositionHistoryByFlightNo(flight_no)

        # If the flight has histories then need to covert it to json and store in the position histories variable
        if histories is not None:
            position_histories = [item.json() for item in histories]

        # make the response data
        data = {
            "flight_information":flight,
            "position_histories":position_histories
        }
        # return the response success with 200 http code
        return {
            "status":"success",
            "data":data
        },200

