from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
from models.Aircraft import Aircraft
class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer,primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    aircraft = db.relationship('Aircraft', backref='flights')
    flight_no = db.Column(db.String,unique=True)
    src = db.Column(db.String,nullable=True)
    destination = db.Column(db.String,nullable=True)
    flight_callsign = db.Column(db.String,nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=True)

    def __init__(self, aircraft_id, flight_no, src=None, destination=None, flight_callsign=None):
        self.aircraft_id = aircraft_id
        self.flight_no = flight_no
        self.src = src
        self.destination = destination
        self.flight_callsign = flight_callsign

    def json(self):
        return {
            "id":self.id,
            "aircraft":(self.aircraft).json(),
            "flight_no":self.flight_no,
            "src":self.src,
            "destination":self.destination,
            "flight_callsign":self.flight_callsign,
            "created_at":(self.created_at).strftime("%d-%m-%Y, %H:%M:%S")
        }

    @classmethod
    def getAllFlights(cls):
        return db.session.query(cls).all()

    @classmethod
    def getFlightByFlightNo(cls, flight_no):
        return cls.query.filter_by(flight_no=flight_no).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
