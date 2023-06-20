from flask_restful import Resource
import requests
from helpers.AircraftHelper import findOrCreateAircraft
from helpers.FlightHelper import generateFlightNo,flightDataValidator
from helpers.FlightStatusHelper import flight_to_destination_distance, bd_airports_icao, is_in_bangladesh
from models.Flight import Flight
from models.FlightPosition import FlightPosition
from models.SensorData import SensorData
from celery_config import update_flight_status_for_bangladeshi_landings, update_bangladeshi_fir_flight_status, update_non_bangladeshi_fir_flight_status

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
                    
                    # Check if Fli_dst airport is bangladeshi airport
                    if flightInfoFromSensor['dst'] is not None and (flightInfoFromSensor['dst'] in bd_airports_icao):
                        print("destination bd airports")
                        update_flight_status_for_bangladeshi_landings.delay(flightInfoFromSensor, flight_no) # flight status celery task
                        
                        item['flight_no'] = flight_no
                        hex_set.add(hex_value)
                        unique_data.append(item)
                    else:
                        is_in_bangladeshi_area = is_in_bangladesh(flightInfoFromSensor['lat'], flightInfoFromSensor['lon'])

                        if is_in_bangladeshi_area:
                            print("using bangladeshi fir",flightInfoFromSensor['fli'])
                            update_bangladeshi_fir_flight_status.delay(flightInfoFromSensor, flight_no)

                            item['flight_no'] = flight_no
                            hex_set.add(hex_value)
                            unique_data.append(item)
                        else:
                            print("not using bangladeshi fir",flightInfoFromSensor['fli'])
                            update_non_bangladeshi_fir_flight_status.delay(flight_no)

        return {
            "status": "success",
            "data": unique_data
        }