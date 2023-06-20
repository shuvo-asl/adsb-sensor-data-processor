from datetime import datetime as dt
def generateFlightNo(flight):
    return (str(flight['reg']+"_") if flight['reg'] is not None else "") + flight['fli']+"_"+str(dt.now().strftime("%d%m%Y"))

def flightDataValidator(flight):
    lat = flight['lat'] is not None
    lon = flight['lon'] is not None
    fli = flight['fli'] is not None
    return (lat and lon and fli)