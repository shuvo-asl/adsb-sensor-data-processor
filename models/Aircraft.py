from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer,primary_key=True)