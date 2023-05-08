from flask_restful import Resource
import datetime
import requests
from helpers.AircraftHelper import findOrCreateAircraft
from helpers.FlightHelper import generateFlightNo,flightDataValidator
from models.Flight import Flight
from models.FlightPosition import FlightPosition
class LivePosition(Resource):
    def get(self):
        flightInfoFromSensor = {
            "uti": 1683539608,
            "ns": 44729828,
            "hex": "800C3B",
            "fli": "LLR742",
            "src": "A",
            "ava": "A",
            "lat": 22.96037,
            "lon": 89.52279,
            "alt": 16000,
            "gda": "A",
            "spd": 215,
            "trk": 253,
            "vrt": 64,
            "tmp": None,
            "wsp": None,
            "wdi": None,
            "cat": "A0",
            "org": None,
            "dst": None,
            "opr": "LLR",
            "typ": "AT76",
            "reg": "VT-RKF",
            "dis": 15.5,
            "dbm": -75,
            "cou": "Indi",
            "squ": "2605",
            "tru": 1273,
            "lla": 0,
            "alr": 0,
            "spi": False,
            "pic": 11,
            "altg": 16800
        };



        khulna = requests.get("http://192.168.201.3/aircraftlist.json").json();
        dhaka = requests.get("http://192.168.30.27/aircraftlist.json").json();
        #
        # Combine the JSON objects into a single list
        data_list = []
        data_list.extend(khulna)
        data_list.extend(dhaka)
        hex_set = set()
        unique_data = []
        for item in data_list:
            hex_value = item['hex']
            if hex_value not in hex_set:
                flightInfoFromSensor = item

                if flightDataValidator(flightInfoFromSensor):
                    aircraft_details = findOrCreateAircraft(flightInfoFromSensor)
                    flight_no = generateFlightNo(flightInfoFromSensor)
                    flight = Flight.getFlightByFlightNo(flight_no)
                    if flight is None:
                        flight = Flight(**{"aircraft_id": aircraft_details['id'], "flight_no": flight_no,
                                           "src": flightInfoFromSensor['src']
                            , "destination": flightInfoFromSensor['dst'],
                                           "flight_callsign": flightInfoFromSensor['fli']})
                        flight.save()
                    flight = flight.json()

                    flightPositionInstance = FlightPosition(**{
                        "flight_id": flight['id'],
                        "lat": flightInfoFromSensor['lat'],
                        'lon': flightInfoFromSensor['lon'],
                        "altitude": flightInfoFromSensor['alt'],
                        "speed": flightInfoFromSensor['spd'],
                        "angle": flightInfoFromSensor['trk'],
                        "response_text": flightInfoFromSensor,
                    })
                    flightPositionInstance.save()

                    item['flight_no'] =flight_no

                    hex_set.add(hex_value)
                    unique_data.append(item)
        return {
            "status": "success",
            "data": unique_data
        }