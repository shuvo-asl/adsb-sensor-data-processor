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
def handle_flight_status(new_flight_status):
    flight_data['flight_status'] = new_flight_status
    # print('Received flight_status:', flight_data['flight_status'])
    with app.app_context():
        # while True:
            if flight_data['flight_status'] is not None:
                flights = Flight.getFlightByStatus(flight_data['flight_status'])
            else:
                flights = []
            
            updated_flights = []

            if len(flights) > 0:
                if flight_data['flight_status'] == 'running':
                    for fli in flights:
                        last_flight_position = FlightPosition.query \
                        .join(Flight) \
                        .filter(Flight.id == fli.id) \
                        .order_by(FlightPosition.id.desc()) \
                        .first()

                        flight_json = fli.json()
                        flight_json['lat'] = last_flight_position.lat
                        flight_json['lon'] = last_flight_position.lon

                        updated_flights.append(flight_json)
                else:
                    for fli in flights:
                        flight_json = fli.json()
                        flight_json['lat'] = None
                        flight_json['lon'] = None

                        updated_flights.append(flight_json)
                # flights = [flight.json() for flight in flights]

            socketio.emit('data', updated_flights)
            # time.sleep(2)

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