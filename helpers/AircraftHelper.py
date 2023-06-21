from models.Aircraft import Aircraft
from models.AircraftType import AircraftType
from db import db

# This method is able to findOrCreateAircraft form the database
def findOrCreateAircraft(data):
    aircraft = Aircraft.findAircraftByRegistrationNumber(data['reg']);

    if aircraft is not None:
        return aircraft.json()

    aircraftType = AircraftType.findAircraftTypeByName(data['typ'])

    if aircraftType is None:
        aircraftType = AircraftType(**{
            'name':data['typ']
        })
        aircraftType.save()

    aircraftType = aircraftType.json()

    aircraft = Aircraft(**{
        "aircraft_type_id":aircraftType['id'],
        "registration_number":data['reg']
    })
    aircraft.save();

    return aircraft.json()
