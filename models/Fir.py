from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
class Fir(db.Model):
    __tablename__ = 'fir'
    id = db.Column(db.Integer,primary_key=True)