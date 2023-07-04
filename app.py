from bootstrap import bootstrap
from flask_restful import Api
from views.Welcome import Welcome, Rnd
from views.LivePosition import LivePosition
from views.FlightPositionView import FlightPositionView
from views.AirportView import AirportView
from views.FlightView import FlightView
from config.env import getEnv
app = bootstrap.app
api = Api(app)

# Add project routes
api.add_resource(Welcome,'/')
api.add_resource(Rnd,'/rnd')
api.add_resource(LivePosition,'/live')
api.add_resource(FlightPositionView,'/history/<flight_no>')
api.add_resource(AirportView,'/airport','/airport/<iso_code>')
api.add_resource(FlightView,'/flight','/flight/<flight_status>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=getEnv('APP_PORT'), debug=True, threaded=False)
    # app.run()