from flask_restful import Resource
import requests
from helpers.AircraftHelper import findOrCreateAircraft
from helpers.FlightHelper import generateFlightNo,flightDataValidator
from models.Flight import Flight
from models.FlightPosition import FlightPosition
from models.SensorData import SensorData

from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates from degrees to radians
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    # Radius of the Earth in kilometers
    earth_radius = 6371

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = earth_radius * c

    return distance

bd_airports_details = {
    "VGBR": {
        "id": 605,
        "name": "Barisal Airport",
        "iata": "BZL",
        "icao": "VGBR",
        "latitude": "22.801",
        "longitude": "90.3012",
        "altitude": "23",
        "timezone": "6",
        "color": "#8ea824",
        "city": "Barisal"
    },
    "VGEG":{
        "id": 6708,
        "name": "Shah Amanat International Airport",
        "iata": "CGP",
        "icao": "VGEG",
        "latitude": "22.249611",
        "longitude": "91.813286",
        "altitude": "12",
        "timezone": "6",
        "color": "#45ab26",
        "city": "Chittagong"
    },
    "VGCB":{
        "id": 1606,
        "name": "Cox's Bazar Airport ",
        "iata": "CXB",
        "icao": "VGCB",
        "latitude": "21.451944",
        "longitude": "91.963889",
        "altitude": "12",
        "timezone": "6",
        "color": "#2ee80e",
        "city": "Cox's Bazar"
    },
    "VGHS":{
        "id": 2842,
        "name": "Hazrat Shahjalal International Airport",
        "iata": "DAC",
        "icao": "VGHS",
        "latitude": "23.842778",
        "longitude": "90.400556",
        "altitude": "30",
        "timezone": "6",
        "color": "#4909eb",
        "city": "Dhaka"
    },
    "VGTJ":{
        "id": 7303,
        "name": "Tejgaon Airport",
        "iata": "",
        "icao": "VGTJ",
        "latitude": "23.778783",
        "longitude": "90.382689",
        "altitude": "24",
        "timezone": "6",
        "color": "#336606",
        "city": "Dhaka"
    },
    "VGIS":{
        "id": 3130,
        "name": "Ishwardi Airport",
        "iata": "IRD",
        "icao": "VGIS",
        "latitude": "24.153197",
        "longitude": "89.048622",
        "altitude": "45",
        "timezone": "6",
        "color": "#eb7373",
        "city": "Ishurdi"
    },
    "VGJR":{
        "id": 3221,
        "name": "Jessore Airport",
        "iata": "JSR",
        "icao": "VGJR",
        "latitude": "23.1838",
        "longitude": "89.160833",
        "altitude": "20",
        "timezone": "6",
        "color": "#f0d11f",
        "city": "Jessore"
    },
    "VGKN":{
        "id": 3535,
        "name": "Khulna Airport",
        "iata": "KHL",
        "icao": "VGKN",
        "latitude": "22.464897",
        "longitude": "89.351261",
        "altitude": "0",
        "timezone": "6",
        "color": "#ab0000",
        "city": "Khulna"
    },
    "VGRJ":{
        "id": 6709,
        "name": "Shah Makhdum Airport",
        "iata": "RJH",
        "icao": "VGRJ",
        "latitude": "24.437219",
        "longitude": "88.616511",
        "altitude": "64",
        "timezone": "6",
        "color": "#0c84d4",
        "city": "Rajshahi"
    },
    "VGSD":{
        "id": 6405,
        "name": "Saidpur Airport",
        "iata": "SPD",
        "icao": "VGSD",
        "latitude": "25.759167",
        "longitude": "88.908611",
        "altitude": "125",
        "timezone": "6",
        "color": "#a10345",
        "city": "Saidpur"
    },
    "VGSY":{
        "id": 5576,
        "name": "Osmani International Airport ",
        "iata": "ZYL",
        "icao": "VGSY",
        "latitude": "24.963333",
        "longitude": " 91.866944",
        "altitude": "50",
        "timezone": "6",
        "color": "#8c2e99",
        "city": "Sylhet"
    },
    "VGSH":{
        "id": 8230,
        "name": "Shamshernagar Airport",
        "iata": "ZHM",
        "icao": "VGSH",
        "latitude": "24.39825",
        "longitude": "91.916944",
        "altitude": "",
        "timezone": "6",
        "color": "#000000",
        "city": "Sylhet"
    },
    "VGCM":{
        "id": 8229,
        "name": "Comilla Airport",
        "iata": "CLA",
        "icao": "VGCM",
        "latitude": "23.436806",
        "longitude": "91.189861",
        "altitude": "",
        "timezone": "6",
        "color": "#f7ef0a",
        "city": "Comilla"
    }
}

bd_airports_icao = ["VGBR","VGEG","VGCB","VGHS","VGTJ","VGIS","VGJR","VGKN","VGRJ","VGSD","VGSY","VGSH","VGCM"]

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

                    # Check if Fli_dst airport is bangladeshi airport
                    if flightInfoFromSensor['dst'] in bd_airports_icao:
                        count+=1
                        destination_airport_details = bd_airports_details[flightInfoFromSensor['dst']]
                        print("Yes, Destination of the aircraft is a Bangladeshi Airport. Airport Name: ", destination_airport_details['name'])

                        # distance from flight to destination airport in km

                        distance_from_flight_to_dst_airport = calculate_distance(flightInfoFromSensor['lat'], flightInfoFromSensor['lon'], destination_airport_details["latitude"], destination_airport_details["longitude"])

                        print("The distance between flight and dst airportis:", distance_from_flight_to_dst_airport, " kilometers.\n")

                    aircraft_details = findOrCreateAircraft(flightInfoFromSensor)
                    flight_no = generateFlightNo(flightInfoFromSensor)
                    flight = Flight.getFlightByFlightNo(flight_no)
                    if flight is None:
                        flight = Flight(**{"aircraft_id": aircraft_details['id'], "flight_no": flight_no,
                                           "src": flightInfoFromSensor['org']
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
        print("count", count, " \n")
        return {
            "status": "success",
            "data": unique_data
        }