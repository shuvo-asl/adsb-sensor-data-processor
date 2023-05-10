from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
from models.Location import Location


class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    iata = db.Column(db.String(10))
    icao = db.Column(db.String(10))
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    altitude = db.Column(db.String(255))
    timezone = db.Column(db.String(255))
    dst = db.Column(db.String(255))
    tzdbtz = db.Column(db.String(255))
    color = db.Column(db.String(20))
    is_visible = db.Column(db.Boolean, nullable=False, default=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    comment = db.Column(db.String(255))
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(DateTime, nullable=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
    
    location = db.relationship('Location', backref='airports')


    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "city_id":self.city_id,
            "iata":self.iata,
            "icao":self.icao,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "altitude":self.altitude,
            "timezone":self.timezone,
            "dst":self.dst,
            "tzdbtz":self.tzdbtz,
            "color":self.color,
            "is_visible":self.is_visible,
            "comment":self.comment,
            "created_at":(self.created_at).strftime("%d-%m-%Y, %H:%M:%S")
        }

    @classmethod
    def getAllAirports(cls):
        return db.session.query(cls).filter(cls.is_deleted == 0).all()
    @classmethod
    def getAirportByIcao(cls,icao):
        airport =  db.session.query(cls).filter(cls.icao==icao).first()
        if airport is not None:
            airport = airport.json()
        return airport


