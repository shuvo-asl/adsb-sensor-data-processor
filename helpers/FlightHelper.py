def generateFlightNo(flight):
    return flight['hex']

def flightDataValidator(flight):
    lat = flight['lat'] is not None
    lon = flight['lon'] is not None
    type = flight['typ'] is not None
    reg = flight['reg'] is not None
    return (lat and lon and type and reg)