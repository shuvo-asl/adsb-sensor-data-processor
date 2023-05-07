from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer,primary_key=True)