import os
from bootstrap import bootstrap
from flask_sqlalchemy import SQLAlchemy
app = bootstrap.app
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@db:5432/{}".format('postgres','password','adsb_fdp')
db = SQLAlchemy(app)