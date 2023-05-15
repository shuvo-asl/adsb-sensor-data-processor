from datetime import datetime as dt
def generateFlightNo(flight):
    return flight['reg']+"_"+flight['fli']+"_"+str(dt.now().strftime("%d%m%Y"))

def flightDataValidator(flight):
    lat = flight['lat'] is not None
    lon = flight['lon'] is not None
    type = flight['typ'] is not None
    reg = flight['reg'] is not None
    org = flight['org'] is not None
    dst = flight['dst'] is not None
    return (lat and lon and type and reg and org and dst)