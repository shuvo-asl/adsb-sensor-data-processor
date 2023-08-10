from celery import Celery
from celery.schedules import crontab
from time import sleep
from helpers.FlightStatusHelper import flight_to_destination_distance
from models.Flight import Flight
from models.FlightPosition import FlightPosition
from helpers.AircraftHelper import findOrCreateAircraft
from bootstrap import bootstrap
from db import db
from datetime import datetime, timedelta
from config.env import getEnv
import requests
import logging
from logging.handlers import RotatingFileHandler
import os

app = bootstrap.app

# Celery configuration
app.config.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0'
)

stol_distance = 1  # STOL distance 1 km
stol_speed = 50  # STOL speed 50 nautical miles

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['broker_url'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = make_celery(app)

# Configure logging
log_folder = 'logs'
log_file = os.path.join(log_folder, f'pod_task_{datetime.now():%Y-%m-%d}.log')
log_level = logging.DEBUG

# Create the log folder if it doesn't exist
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Use RotatingFileHandler for log rotation with negative backupCount
handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=-1)
handler.setLevel(log_level)


# Create a log format with a timestamp
log_format = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

app.logger.addHandler(handler)

def get_pod_access_token(api_url, pod_client_secret_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {pod_client_secret_key}',
    }
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
        else:
            result = {"error": f"There's a {response.status_code} error with your request"}

    except Exception as e:
        result = {"error": str(e)}
    
    return result
    


def get_flights_by_date(flight_url, pod_access_token, previous_date):

    headers = {
        'Authorization': f'Bearer {pod_access_token}',
    }
    try:
        data={"date":previous_date}
        response = requests.post(flight_url, data=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
        else:
            result = {"error": f"There's a {response.status_code} error with your request"}

    except Exception as e:
        result = {"error": str(e)}
    
    return result
    


def get_flights_details_by_date_callsign_and_aircraft_no(flight_details_url, pod_access_token, previous_date, call_sign, aircraft_no):

    headers = {
        'Authorization': f'Bearer {pod_access_token}',
    }
    try:
        # data={"date":previous_date, "call_sign": call_sign, "aircraft_no":aircraft_no}
        data={"date":previous_date, "call_sign": call_sign}
        response = requests.post(flight_details_url, data=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
        else:
            result = {"error": f"There's a {response.status_code} error with your request"}

    except Exception as e:
        result = {"error": str(e)}
    
    return result


def send_flights_public_url(update_flight_url, pod_access_token, previous_date, call_sign, aircraft_no, public_url):

    headers = {
        'Authorization': f'Bearer {pod_access_token}',
    }
    try:
        data={"date":previous_date, "call_sign": call_sign, "aircraft_no":aircraft_no}
        
        response = requests.post(update_flight_url, data=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
        else:
            result = {"error": f"There's a {response.status_code} error with your request"}

    except Exception as e:
        result = {"error": str(e)}
    
    return result
    


@celery_app.task
def pod_task():
    app.logger.info('Task started')
    pod_client_secret_key = getEnv('POD_CLIENT_SECRET_KEY')

    api_url = getEnv('POD_ACCESS_TOKEN_API')
    flight_url = getEnv('FLIGHT_URL')
    flight_details_url = getEnv('FLIGHT_DETAILS_URL')
    update_flight_url = getEnv('UPDATE_FLIGHT_URL')
    adsb_public_url = getEnv('ADSB_FLIGHT_PUBLIC_URL')

    pod_access_token = get_pod_access_token(api_url, pod_client_secret_key)
    pod_access_token = pod_access_token['access_token']

    today = datetime.today()
    previous_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')

    my_flights = Flight.getCompletedFlightsByStatusAndDate('completed', previous_date)

    # previous_date = (today + timedelta(days=3)).strftime('%Y-%m-%d') # this is for testing, hide it in production

    # getting flight from pod of previous date
    try:
        pod_flights = get_flights_by_date(flight_url, pod_access_token, previous_date) 
        app.logger.info(f'Found flights from pod successfully')
    except Exception as e:
        app.logger.error(f'Exception in getting flights from pod')
        return False
    
    if 'error' not in pod_flights:

        if len(pod_flights) > 0:
            # temporary storing all those pod flights in my stored adsb database's flight. 
            common_flights = [] 
            for flight in pod_flights:
                # finding pod flights in my stored adsb database's flight. 
                res = Flight.findCompletedFlightsByCallsignRegNoAndDate(flight['call_sign'], flight['aircraft_no'], previous_date) 
                if res is not None:
                    common_flights.append(res)
        
            final_flights = []
            for fli in common_flights:
                
                # getting flights details from pod
                try:
                    pod_flights_details = get_flights_details_by_date_callsign_and_aircraft_no(flight_details_url, pod_access_token, previous_date, fli.flight_callsign, fli.aircraft.registration_number)
                    app.logger.info(f"Found flight's details from pod, callsign: {fli.flight_callsign}")
                except Exception as e:
                    app.logger.error(f'Exception in getting flights details from pod')

                # if flight details from pod is matched with my requesting flight without error, then store details in flight table
                if pod_flights_details and ('error' not in pod_flights_details):
                    if pod_flights_details['call_sign'] == fli.flight_callsign:    # commented for debug mode, implemented for live mode.
                        if 'flight_itinerary' in pod_flights_details:
                            fli.src = pod_flights_details['flight_itinerary']['flight_leg_1']['departure']['icao']
                            fli.destination = pod_flights_details['flight_itinerary']['flight_leg_1']['arrival']['icao']
                            fli.pod_response = pod_flights_details
                            fli.save()
                            app.logger.info(f"Adsb Flight updated with pod flight details, callsign: {fli.flight_callsign}")
                            final_flights.append(fli) # storing those flights which are being updated by pod flights data. Stored for sending public url

            # sending flight public url to another api to view flight's route
            for final_fli in final_flights:
                public_url = str(adsb_public_url) + final_fli.flight_no
                try:
                    update_pod_flight = send_flights_public_url(update_flight_url, pod_access_token, previous_date, final_fli.flight_callsign, final_fli.aircraft.registration_number, public_url)
                    app.logger.info(f"Pod Flight updated with public Url, callsign: {final_fli.flight_callsign}")
                except Exception as e:
                    app.logger.error(f"Exception in updating flight's public url in pod, callsign: {final_fli.flight_callsign}")

                if 'error' in update_pod_flight:
                    app.logger.error(f"{update_pod_flight['error']}. Error from updating public url id pod, callsign: {final_fli.flight_callsign}")
            
        else:
            app.logger.info(f'Flights not found on the previous day.')

    app.logger.info('Task finished')
    return True


# Schedule the task to run every day at 12:05 AM using Celery Beat
celery_app.conf.beat_schedule = {
    'daily-task-scheduler': {
        'task': 'celery_config.pod_task',
        'schedule': crontab(hour=0, minute=5),  # Schedule the task to run every day at 12:05 AM
        # 'schedule': timedelta(seconds=10),  # Schedule the task to run every 30 seconds
    },
}


@celery_app.task
def update_flight_status_for_bangladeshi_landings(flightInfoFromSensor, flight_no, order_number):
    flight_status = "pending"
    try:
        fli_to_des_distance = flight_to_destination_distance(flightInfoFromSensor)
        if flightInfoFromSensor['spd'] <= stol_speed and fli_to_des_distance <= stol_distance:
            flight_status = "completed"
        else:
            flight_status = "running"

        print("Completed from update_flight_status_for_bangladeshi_landings")
        
        flight_and_its_position_store(flightInfoFromSensor, flight_status, flight_no, order_number)

        return True

    except Exception as e:
        print("Exception from update_flight_status_for_bangladeshi_landings", str(e))
        return False


def flight_and_its_position_store(flightInfoFromSensor, flight_status, flight_no, order_number):
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
            flight.updated_at = datetime.utcnow()
            db.session.commit()

        flight = flight.json()

        flightPositionInstance = FlightPosition(**{
            "flight_id": flight['id'],
            "lat": flightInfoFromSensor['lat'],
            'lon': flightInfoFromSensor['lon'],
            "altitude": flightInfoFromSensor['alt'],
            "speed": flightInfoFromSensor['spd'],
            "angle": flightInfoFromSensor['trk'],
            "order_number": order_number,
            "response_text": flightInfoFromSensor,
        })

        flightPositionInstance.save()
        print("Completed from flight_and_its_position_store",flight_status, flight_no)
        return True

    except Exception as e:
        print("Exception from flight_and_its_position_store", str(e))
        return False


@celery_app.task
def update_bangladeshi_fir_flight_status(flightInfoFromSensor, flight_no, order_number):
    try:
        flight_status = "running"
        flight_and_its_position_store(flightInfoFromSensor, flight_status, flight_no, order_number)

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
            flight.updated_at = datetime.utcnow()
            db.session.commit()
        print("Completed from update_non_bangladeshi_fir_flight_status")

        return True

    except Exception as e:
        print("Exception from update_non_bangladeshi_fir_flight_status", str(e))
        return False
