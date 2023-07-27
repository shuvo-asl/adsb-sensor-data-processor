from db import db
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
from models.Aircraft import Aircraft
from datetime import date, datetime, timedelta
from sqlalchemy import JSON
from sqlalchemy import and_

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer,primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    aircraft = db.relationship('Aircraft', backref='flights')
    flight_no = db.Column(db.String,unique=True)
    src = db.Column(db.String,nullable=True)
    destination = db.Column(db.String,nullable=True)
    status = db.Column(db.Enum('running', 'completed', 'pending',  name='flight_status_enum'), nullable=False, default='pending')
    flight_callsign = db.Column(db.String,nullable=True)
    pod_response = db.Column(JSON,nullable=True)
    created_at = Column(DateTime, default= datetime.utcnow())
    updated_at = Column(DateTime, nullable=True)

    # def __init__(self, aircraft_id, flight_no, src=None, destination=None, flight_callsign=None):
    #     self.aircraft_id = aircraft_id
    #     self.flight_no = flight_no
    #     self.src = src
    #     self.destination = destination
    #     self.flight_callsign = flight_callsign

    def json(self):
        return {
            "id":self.id,
            "aircraft":(self.aircraft).json(),
            "flight_no":self.flight_no,
            "src":self.src,
            "destination":self.destination,
            "flight_callsign":self.flight_callsign,
            "created_at":(self.created_at).strftime("%d-%m-%Y, %H:%M:%S"),
            "updated_at":(self.updated_at).strftime("%d-%m-%Y, %H:%M:%S") if self.updated_at is not None else None,
            "status":self.status,
            "pod_response":self.pod_response,
        }

    @classmethod
    def getAllFlights(cls):
        return db.session.query(cls).all()

    @classmethod
    def getFlightByFlightNo(cls, flight_no):
        return cls.query.filter_by(flight_no=flight_no).first()
    @classmethod
    def getFlightByStatus(cls, status):
        # flights = cls.query.filter_by(status=status).order_by(cls.updated_at.desc()).all()
        flights = cls.query.filter_by(status=status).order_by(cls.id.desc()).all()
        return flights

    @classmethod
    def getCompletedFlightsByStatusAndDate(cls, status, date):
        flights = cls.query.filter_by(status=status).filter(db.func.date(cls.updated_at) == date).order_by(cls.id.desc()).all()
        return flights

    @classmethod
    def findCompletedFlightsByCallsignRegNoAndDate(cls, flight_callsign, registration_number, date):
        flights = cls.query.join(Aircraft).filter(
            and_(
                cls.flight_callsign == flight_callsign,
                Aircraft.registration_number == registration_number,
                cls.status == 'completed',
                db.func.date(cls.updated_at) == date,
            )
        ).order_by(cls.id.desc()).first()
        return flights

    @classmethod
    def getRunningFlights(cls):
        time_threshold = datetime.utcnow() - timedelta(seconds=30)

        flights = cls.query.filter_by(status='running').filter(cls.updated_at >= time_threshold).order_by(cls.id.desc()).all()
        return flights

    def save(self):
        db.session.add(self)
        db.session.commit()
