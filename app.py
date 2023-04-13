from flask import Flask
from bootstrap import bootstrap
from db import db
from flask_restful import Api
from views.SensorView import SensorView
app = bootstrap.app
api = Api(app)
api.add_resource(SensorView,'/sensor');
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)