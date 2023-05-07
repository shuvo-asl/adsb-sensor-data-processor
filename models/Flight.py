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

    def json(self):
        return {
            "id":self.id,
            "aircraft":str(self.aircraft),
            "flight_no":self.flight_no,
            "src":self.src,
            "destination":self.destination,
            "flight_callsign":self.flight_callsign,
            "created_at":(self.created_at).strftime("%d-%m-%Y, %H:%M:%S")
        }

    @classmethod
    def getAllFlights(cls):
        return db.session.query(cls).all()

