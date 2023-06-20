import os
from bootstrap import bootstrap
from flask_sqlalchemy import SQLAlchemy
from config.env import getEnv
app = bootstrap.app

db_driver = getEnv("DB_DRIVER")
db_user = getEnv("DB_USER")
db_password = getEnv("DB_PASSWORD")
db_host = getEnv("DB_HOST")
db_port = getEnv("DB_PORT")
db_name = getEnv("DB_NAME")

# FOR MYSQL
if db_driver == "mysql":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user,db_password,db_host,db_name)

# FOR POSTGRESQL
elif db_driver == "postgres":
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(db_user,db_password,db_host,db_port,db_name)

else:
    raise Exception("Provide Invalid Database Driver")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)