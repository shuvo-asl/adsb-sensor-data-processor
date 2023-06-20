from math import radians, sin, cos, sqrt, atan2

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


def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates from degrees to radians
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    earth_radius_km = 6371
    conversion_factor = 0.62137119

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance_km = earth_radius_km * c
    distance_miles = distance_km * conversion_factor

    return distance_km


# distance from flight to destination airport(bd airports only)
def flight_to_destination_distance(flightInfoFromSensor=None):
    if flightInfoFromSensor is not None:
        destination_airport_details = bd_airports_details[flightInfoFromSensor['dst']]
        if destination_airport_details is not None:
            distance_from_flight_to_dst_airport = calculate_distance(flightInfoFromSensor['lat'], flightInfoFromSensor['lon'], destination_airport_details["latitude"], destination_airport_details["longitude"])

            return distance_from_flight_to_dst_airport