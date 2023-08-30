from flask_restful import Resource
from models.FlightPosition import FlightPosition
from models.Flight import Flight
from models.Airport import Airport
from models.SensorData import SensorData
from models.OrderNumber import Order
from datetime import date, datetime, timedelta
from helpers.FlightHelper import generateFlightNo,flightDataValidator
import requests
from requests.exceptions import RequestException
from helpers.FlightStatusHelper import flight_to_destination_distance, bd_airports_icao, is_in_bangladesh, is_points_in_bangladesh
from celery_config import update_flight_status_for_bangladeshi_landings, update_bangladeshi_fir_flight_status, update_non_bangladeshi_fir_flight_status

from shapely.geometry import Point

PRIORITY_HIGH = 0
PRIORITY_NORMAL = 5
PRIORITY_LOW = 10

def FlightStatusHelper(new_flight_status, filter_date = None):
    flights = []

    if new_flight_status is not None:

        if new_flight_status == 'running':
            flights = Flight.getRunningFlights()

        else:
            if filter_date is not None and filter_date!='':
                flight_date = datetime.strptime(filter_date, '%Y-%m-%d').date()
                flights = Flight.getCompletedFlightsByStatusAndDate(new_flight_status, flight_date)
            else:
                flights = Flight.getFlightByStatus(new_flight_status)
    
    updated_flights = []

    if len(flights) > 0:
        if new_flight_status == 'running':
            for fli in flights:
                last_flight_position = FlightPosition.query \
                .join(Flight) \
                .filter(Flight.id == fli.id) \
                .order_by(FlightPosition.id.desc()) \
                .first()

                flight_json = fli.json()
                flight_json['lat'] = last_flight_position.lat
                flight_json['lon'] = last_flight_position.lon

                updated_flights.append(flight_json)
        else:
            for fli in flights:
                flight_json = fli.json()
                flight_json['lat'] = None
                flight_json['lon'] = None

                updated_flights.append(flight_json)

    return updated_flights



def FlightPositionHelper(flight_no):

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
    return {"status":"success", "data":data}


def FlightsLiveLocation():
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
        response = requests.get("http://45.125.223.124/aircraftlist.json", timeout=1)
        response.raise_for_status()
        chittagong = response.json()
        data_list.extend(chittagong)
    except RequestException as e:
        print('Error from sensor Chittagong:', str(e))

    for item in data_list:

        hex_value = item['hex']
        if hex_value not in hex_set:
            flightInfoFromSensor = item
            if flightDataValidator(flightInfoFromSensor):
                count+=1
                flight_no = generateFlightNo(flightInfoFromSensor)
                
                # Check if Fli_dst airport is bangladeshi airport
                if flightInfoFromSensor['dst'] is not None and (flightInfoFromSensor['dst'] in bd_airports_icao):
                    item['flight_no'] = flight_no
                    hex_set.add(hex_value)
                    unique_data.append(item)
                else:
                    # is_in_bangladeshi_area = is_in_bangladesh(flightInfoFromSensor['lat'], flightInfoFromSensor['lon'])
                    is_in_bangladeshi_area = is_points_in_bangladesh(Point(flightInfoFromSensor['lon'],flightInfoFromSensor['lat']))

                    if is_in_bangladeshi_area:
                        item['flight_no'] = flight_no
                        hex_set.add(hex_value)
                        unique_data.append(item)

    return unique_data


def StoreAndReturnFlightsLiveLocation():
    data_list = []
    hex_set = set()
    unique_data = []

    try:
        response = requests.get("http://192.168.30.27/aircraftlist.json", timeout=1)
        response.raise_for_status()
        dhaka = response.json()
        data_list.extend(dhaka)
    except RequestException as e:
        print('Error from sensor Dhaka:', str(e))

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

                order = Order.get_singleton()
                order_json = order.json()
                order_number = order_json['order_number']
                order.order_number += 1
                order.save()

                flight_no = generateFlightNo(flightInfoFromSensor)

                if flightInfoFromSensor['dst'] is not None and (flightInfoFromSensor['dst'] in bd_airports_icao):
                    update_flight_status_for_bangladeshi_landings.apply_async(args=[flightInfoFromSensor, flight_no, order_number], priority=PRIORITY_NORMAL)
                    item['flight_no'] = flight_no
                    hex_set.add(hex_value)
                    unique_data.append(item)
                else:
                    is_in_bangladeshi_area = is_points_in_bangladesh(Point(flightInfoFromSensor['lon'],flightInfoFromSensor['lat']))

                    if is_in_bangladeshi_area:
                        update_bangladeshi_fir_flight_status.apply_async(args=[flightInfoFromSensor, flight_no, order_number], priority=PRIORITY_HIGH)
                        item['flight_no'] = flight_no
                        hex_set.add(hex_value)
                        unique_data.append(item)
                    else:
                        update_non_bangladeshi_fir_flight_status.apply_async(args=[flight_no], priority=PRIORITY_LOW)

    return unique_data