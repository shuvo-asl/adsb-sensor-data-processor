from bootstrap import bootstrap
from flask_restful import Api
from views.SensorView import SensorView
from views.Welcome import Welcome
from views.PositionView import PositionView
app = bootstrap.app
api = Api(app)

api.add_resource(PositionView,'/positions')
api.add_resource(Welcome,'/')
api.add_resource(SensorView,'/sensor');

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)
    app.run()