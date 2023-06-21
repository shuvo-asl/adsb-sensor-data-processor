from datetime import datetime as dt
# Generate filght unique flight number by using using registration call sign and current date
def generateFlightNo(flight):
    return (str(flight['reg']+"_") if flight['reg'] is not None else "") + flight['fli']+"_"+str(dt.now().strftime("%d%m%Y"))

# Validate the flight data to process.
def flightDataValidator(flight):
    lat = flight['lat'] is not None
    lon = flight['lon'] is not None
    fli = flight['fli'] is not None
    return (lat and lon and fli)