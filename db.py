import os
from bootstrap import bootstrap
from flask_sqlalchemy import SQLAlchemy
app = bootstrap.app
# FOR POSTGRESQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@localhost:5432/{}".format('postgres','postgres','adsb_fdp')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/adsb_fdp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)