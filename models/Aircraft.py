# models.py
from db import db
from enum import Enum
import datetime
from sqlalchemy import desc
from models.AircraftType import AircraftType

class PurposeType(Enum):
    Civil = 'Civil'
    Military = 'Military'

class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aircraft_type_id = db.Column(db.Integer, db.ForeignKey('aircraft_types.id'), nullable=False)
    registration_number = db.Column(db.String(250), nullable=False)
    mtow = db.Column(db.Float(precision=2), nullable=True)
    mtow_unit = db.Column(db.Enum('lbs', 'kgs'), nullable=True)
    purpose_type = db.Column(db.Enum(PurposeType), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer,nullable=True)
    updated_by = db.Column(db.Integer,nullable=True)

    aircraft_type = db.relationship('AircraftType', backref='aircrafts')

    def __init__(self, aircraft_type_id, registration_number, mtow=None, mtow_unit=None, purpose_type='Civil'):
        self.aircraft_type_id = aircraft_type_id
        self.registration_number = registration_number
        self.mtow = mtow
        self.mtow_unit = mtow_unit
        self.purpose_type = purpose_type

    def json(self):
        return {
            "id":self.id,
            "aircraft_type_id":self.aircraft_type_id,
            "registration_number":self.registration_number,
            "mtow":self.mtow,
            "mtow_unit":self.mtow_unit,
            "purpose_type":self.purpose_type.value,
            "created_at":(self.created_at).strftime("%d-%m-%Y, %H:%M:%S")
        }

    @classmethod
    def getAllAircrafts(cls):
        return db.session.query(cls).filter(cls.is_deleted == 0).all()

    @classmethod
    def findAircraftByRegistrationNumber(cls,reg_no):
        return db.session.query(cls).filter(cls.registration_number==reg_no).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
