from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.Integer,primary_key=True)