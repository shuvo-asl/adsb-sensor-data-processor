from bootstrap import bootstrap
from flask_restful import Api
from views.Welcome import Welcome, Rnd
from views.LivePosition import LivePosition
from views.FlightPositionView import FlightPositionView
from views.AirportView import AirportView
from views.FlightView import FlightView
from models.Flight import Flight
from models.FlightPosition import FlightPosition
from config.env import getEnv
from flask_socketio import SocketIO, emit
import time
import eventlet
from helpers.SocketHelper import FlightPositionHelper, FlightStatusHelper

from datetime import date, datetime, timedelta

eventlet.monkey_patch()

app = bootstrap.app
api = Api(app)

socketio = SocketIO(app, cors_allowed_origins='*')

flight_data = {
    'flight_status': None
}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('flight_status')
def handle_flight_status(new_flight_status, filter_date = None):
    # with app.app_context():

    data = FlightStatusHelper(new_flight_status, filter_date)
    socketio.emit('data', data)

@socketio.on('flight_no')
def handle_flight_location(flight_no = None):
    flight_data = FlightPositionHelper(flight_no)
    socketio.emit('flight_data', flight_data)


@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    emit('response', 'Server received message: ' + data)

# Add project routes
api.add_resource(Welcome,'/')
api.add_resource(Rnd,'/rnd')
api.add_resource(LivePosition,'/live')
api.add_resource(FlightPositionView,'/history/<flight_no>')
api.add_resource(AirportView,'/airport','/airport/<iso_code>')
api.add_resource(FlightView,'/flight','/flight/<flight_status>')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=getEnv('APP_PORT'), debug=True)
    # app.run()