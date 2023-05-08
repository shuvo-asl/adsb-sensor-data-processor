from bootstrap import bootstrap
from flask_restful import Api
from views.Welcome import Welcome
from views.LivePosition import LivePosition
from views.FlightPositionView import FlightPositionView
app = bootstrap.app
api = Api(app)

api.add_resource(Welcome,'/')
api.add_resource(LivePosition,'/live');
api.add_resource(FlightPositionView,'/history/<flight_no>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=False)
    # app.run()