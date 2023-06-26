from flask_restful import Resource
import requests
from requests.exceptions import RequestException
from helpers.AircraftHelper import findOrCreateAircraft
from helpers.FlightHelper import generateFlightNo,flightDataValidator
from helpers.FlightStatusHelper import flight_to_destination_distance, bd_airports_icao, is_in_bangladesh, is_points_in_bangladesh
from shapely.geometry import Point
from models.Flight import Flight
from models.FlightPosition import FlightPosition
from models.SensorData import SensorData
from celery_config import update_flight_status_for_bangladeshi_landings, update_bangladeshi_fir_flight_status, update_non_bangladeshi_fir_flight_status

class LivePosition(Resource):
    def get(self):
        #
        # Combine the JSON objects into a single list
        data_list = []
        hex_set = set()
        unique_data = []
        count = 0

        try:
            response = requests.get("http://192.168.30.27/aircraftlist.json", timeout=1)
            response.raise_for_status()
            dhaka = response.json()
            data_list.extend(dhaka)
        except RequestException as e:
            print('Error from sensor Dhaka:', str(e))

        try:
            response = requests.get("http://118.179.152.100/aircraftlist.json", timeout=1)
            response.raise_for_status()
            khulna = response.json()
            data_list.extend(khulna)
        except RequestException as e:
            print('Error from sensor Khulna:', str(e))

        try:
            response = requests.get("http://45.125.223.124/aircraftlist.json", timeout=1)
            response.raise_for_status()
            chittagong = response.json()
            data_list.extend(chittagong)
        except RequestException as e:
            print('Error from sensor Chittagong:', str(e))

        for item in data_list:

            # STORE SENSOR DATA INTO HISTORY
            sensor = SensorData(signal_type=item.get('alr', None), **{"data": item})
            sensor.save()

            hex_value = item['hex']
            if hex_value not in hex_set:
                flightInfoFromSensor = item
                if flightDataValidator(flightInfoFromSensor):
                    count+=1
                    flight_no = generateFlightNo(flightInfoFromSensor)
                    
                    # Check if Fli_dst airport is bangladeshi airport
                    if flightInfoFromSensor['dst'] is not None and (flightInfoFromSensor['dst'] in bd_airports_icao):
                        # print("destination bd airports")
                        update_flight_status_for_bangladeshi_landings.delay(flightInfoFromSensor, flight_no) # flight status celery task
                        
                        item['flight_no'] = flight_no
                        hex_set.add(hex_value)
                        unique_data.append(item)
                    else:
                        # is_in_bangladeshi_area = is_in_bangladesh(flightInfoFromSensor['lat'], flightInfoFromSensor['lon'])
                        is_in_bangladeshi_area = is_points_in_bangladesh(Point(flightInfoFromSensor['lon'],flightInfoFromSensor['lat']))

                        if is_in_bangladeshi_area:
                            # print("using bangladeshi fir",flightInfoFromSensor['fli'])
                            update_bangladeshi_fir_flight_status.delay(flightInfoFromSensor, flight_no)

                            item['flight_no'] = flight_no
                            hex_set.add(hex_value)
                            unique_data.append(item)
                        else:
                            # print("not using bangladeshi fir",flightInfoFromSensor['fli'])
                            update_non_bangladeshi_fir_flight_status.delay(flight_no)

        return {
            "status": "success",
            "data": unique_data
        }