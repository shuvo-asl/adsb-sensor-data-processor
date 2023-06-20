from celery import Celery
from time import sleep
from helpers.FlightStatusHelper import flight_to_destination_distance
from models.Flight import Flight
from models.FlightPosition import FlightPosition
from helpers.AircraftHelper import findOrCreateAircraft
from bootstrap import bootstrap
from db import db

app = bootstrap.app

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

stol_distance = 1  # STOL distance 1 km
stol_speed = 50  # STOL speed 50 nautical miles

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = make_celery(app)

@celery_app.task
def update_flight_status_for_bangladeshi_landings(flightInfoFromSensor, flight_no):
    flight_status = "pending"
    try:
        fli_to_des_distance = flight_to_destination_distance(flightInfoFromSensor)
        if flightInfoFromSensor['spd'] <= stol_speed and fli_to_des_distance <= stol_distance:
            flight_status = "completed"
        else:
            flight_status = "running"

        print("Completed from update_flight_status_for_bangladeshi_landings")
        
        flight_and_its_position_store.delay(flightInfoFromSensor, flight_status, flight_no)

        return True

    except Exception as e:
        print("Exception from update_flight_status_for_bangladeshi_landings", str(e))
        return False


@celery_app.task
def flight_and_its_position_store(flightInfoFromSensor, flight_status, flight_no):
    try:
        aircraft_details = findOrCreateAircraft(flightInfoFromSensor)
        flight = Flight.getFlightByFlightNo(flight_no)

        if flight is None:
            flight = Flight(**{"aircraft_id": aircraft_details['id'], "flight_no": flight_no,
                                "src": flightInfoFromSensor['org']
                , "destination": flightInfoFromSensor['dst'],
                                "flight_callsign": flightInfoFromSensor['fli'], "status":flight_status})
            db.session.add(flight)
            db.session.commit()

        else:
            flight.status = flight_status
            db.session.commit()

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
        with app.app_context():
            db.session.add(flightPositionInstance)
            db.session.commit()
        print("Completed from flight_and_its_position_store",flight_status, flight_no)
        return True

    except Exception as e:
        print("Exception from flight_and_its_position_store", str(e))
        return False


@celery_app.task
def update_bangladeshi_fir_flight_status(flightInfoFromSensor, flight_no):
    try:
        flight_status = "running"

        aircraft_details = findOrCreateAircraft(flightInfoFromSensor)
        flight = Flight.getFlightByFlightNo(flight_no)

        if flight is not None:
            flight.status = flight_status
            db.session.commit()

        else:
            flight = Flight(**{"aircraft_id": aircraft_details['id'], "flight_no": flight_no,
                            "src": flightInfoFromSensor['org']
                , "destination": flightInfoFromSensor['dst'],
                            "flight_callsign": flightInfoFromSensor['fli'], "status":flight_status})
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

        print("Completed from update_bangladeshi_fir_flight_status")
        return True

    except Exception as e:
        print("Exception from update_non_bangladeshi_fir_flight_status", str(e))
        return False


@celery_app.task
def update_non_bangladeshi_fir_flight_status(flight_no):
    try:
        
        flight = Flight.getFlightByFlightNo(flight_no)
        flight_position = FlightPosition.getAllPositionHistoryByFlightNo(flight_no)
        if flight is not None and len(flight_position)>0:
            flight.status = "completed"
            db.session.commit()
        print("Completed from update_non_bangladeshi_fir_flight_status")

        return True

    except Exception as e:
        print("Exception from update_non_bangladeshi_fir_flight_status", str(e))
        return False
