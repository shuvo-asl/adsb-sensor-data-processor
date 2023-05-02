from bootstrap import bootstrap
from flask_restful import Api
from views.SensorView import SensorView
from views.PositionHistoryView import PositionHistoryView
from views.Welcome import Welcome
app = bootstrap.app
api = Api(app)

api.add_resource(Welcome,'/')
api.add_resource(SensorView,'/sensor');
api.add_resource(PositionHistoryView,'/history/<unique_code>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)
    # app.run()