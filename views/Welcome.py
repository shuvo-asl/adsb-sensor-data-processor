from flask_restful import Resource
import requests
from helpers.FlightHelper import flightDataValidator
from models.Airport import Airport
from celery_config import process_task
import json
from db import db
class Welcome(Resource):
    def get(self):
        return "ADSB Flight Data Processor is running...";

class RunQueue(Resource):
    def get(self):
        task = "Process the request"  # Modify this based on your task
        process_task.delay(task)
        return "Running"

    def post(self):
        task_data = "Process the request task_data"
        process_task.delay(task_data)
        return {'message': 'Task 2 enqueued'}

class Rnd(Resource):
    def get(self):
        khulna = requests.get("http://118.179.152.100/aircraftlist.json").json();
        dhaka = requests.get("http://192.168.201.3/aircraftlist.json").json();
        #
        # Combine the JSON objects into a single list
        data_list = []
        data_list.extend(khulna)
        data_list.extend(dhaka)
        hex_set = set()
        unique_data = []
        for item in data_list:
            hex_value = item['hex']
            if hex_value not in hex_set:
                flightInfoFromSensor = item
                if flightDataValidator(flightInfoFromSensor):
                    item['org_airport'] = Airport.getAirportByIcao(item['org'])
                    item['dst_airport'] = Airport.getAirportByIcao(item['dst'])
                    hex_set.add(hex_value)
                    unique_data.append(item)
        return {
            "status": "success",
            "data": unique_data
        }