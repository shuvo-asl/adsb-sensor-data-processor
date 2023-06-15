from bootstrap import bootstrap
from flask_restful import Api
from views.Welcome import Welcome,Rnd, RunQueue
from views.LivePosition import LivePosition
from views.FlightPositionView import FlightPositionView
from views.AirportView import AirportView
app = bootstrap.app
api = Api(app)

api.add_resource(Welcome,'/')
api.add_resource(RunQueue,'/run')
api.add_resource(Rnd,'/rnd')
api.add_resource(LivePosition,'/live')
api.add_resource(FlightPositionView,'/history/<flight_no>')
api.add_resource(AirportView,'/airport','/airport/<iso_code>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)
    # app.run()