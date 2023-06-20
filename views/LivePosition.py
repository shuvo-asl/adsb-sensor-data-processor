from flask_restful import Resource
import requests
from helpers.AircraftHelper import findOrCreateAircraft
from helpers.FlightHelper import generateFlightNo,flightDataValidator
from helpers.FlightStatusHelper import flight_to_destination_distance, bd_airports_icao
from models.Flight import Flight
from models.FlightPosition import FlightPosition
from models.SensorData import SensorData
from celery_config import update_flight_status_for_bangladeshi_landings

class LivePosition(Resource):
    def get(self):
        khulna = requests.get("http://118.179.152.100/aircraftlist.json").json();
        dhaka = requests.get("http://192.168.30.27/aircraftlist.json").json();
        #
        # Combine the JSON objects into a single list
        data_list = []
        # data_list.extend(khulna)
        data_list.extend(dhaka)
        hex_set = set()
        unique_data = []
        count = 0
        for item in data_list:

            # STORE SENSOR DATA INTO HISTORY
            sensor = SensorData(signal_type=item.get('alr', None), **{"data": item})
            sensor.save()

            hex_value = item['hex']
            if hex_value not in hex_set:
                flightInfoFromSensor = item
                if flightDataValidator(flightInfoFromSensor):

                    flight_no = generateFlightNo(flightInfoFromSensor)

                    flight_status = "pending"
                    
                    # Check if Fli_dst airport is bangladeshi airport
                    if flightInfoFromSensor['dst'] is not None and (flightInfoFromSensor['dst'] in bd_airports_icao):
                        print("bd airport, update status")
                        update_flight_status_for_bangladeshi_landings.delay(flightInfoFromSensor, flight_no) # flight status celery task
                    else:
                        aircraft_details = findOrCreateAircraft(flightInfoFromSensor)
                        flight = Flight.getFlightByFlightNo(flight_no)

                        if flight is None:
                            flight = Flight(**{"aircraft_id": aircraft_details['id'], "flight_no": flight_no,
                                            "src": flightInfoFromSensor['org']
                                , "destination": flightInfoFromSensor['dst'],
                                            "flight_callsign": flightInfoFromSensor['fli'], "status":flight_status})
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