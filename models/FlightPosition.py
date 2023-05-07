from db import db
import datetime
from sqlalchemy import desc,JSON
from sqlalchemy import Column, DateTime
from models.Flight import Flight
class FlightPosition(db.Model):
    __tablename__ = 'flight_positions'
    id = db.Column(db.Integer,primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    flight = db.relationship('Flight', backref='flight_position')
    lat = db.Column(db.Float(precision=2))
    lon = db.Column(db.Float(precision=2))
    speed = db.Column(db.Float(precision=2),nullable=True)
    angle = db.Column(db.Float(precision=2),nullable=True)
    altitude = db.Column(db.Float(precision=2),nullable=True)
    response_text = db.Column(JSON,nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=True)

    def __int__(self,flight_id,lat,lon,speed,angle,altitude,response,updated_at = None):
        self.flight_id = flight_id
        self.lat = lat
        self.lon = lon
        self.altitude = altitude
        self.speed = speed
        self.angle = angle
        self.response_text = response
        self.updated_at = updated_at

    def json(self):
        return {
            "id":self.id,
            "flight":(self.flight).json(),
            "lat":self.lat,
            'lon':self.lon,
            "altitude":self.altitude,
            "speed":self.speed,
            "angle":self.angle,
            "response_text":self.response_text,
        }
    @classmethod
    def getAllPositions(cls):
        return db.session.query(cls).order_by(desc(cls.id)).all()