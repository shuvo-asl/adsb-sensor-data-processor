from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
class FlightPosition(db.Model):
    __tablename__ = 'flight_positions'
    id = db.Column(db.Integer,primary_key=True)