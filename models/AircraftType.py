from db import db
from enum import Enum
import datetime
from sqlalchemy import desc, Column, DateTime



class AircraftType(db.Model):
    __tablename__ = 'aircraft_types'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    mtow = db.Column(db.Float(precision=2),nullable=True)
    wing_type = db.Column(db.Enum('Fix Wing', 'Helicopter', 'Fixed Wing'), nullable=False)
    mtow_unit = db.Column(db.Enum('lbs', 'kgs'), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=True)
    created_by = db.Column(db.Integer,nullable=True)
    updated_by = db.Column(db.Integer,nullable=True)

    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "mtow":self.mtow,
            "wing_type":self.wing_type,
            "mtow_unit":self.mtow_unit,
            "created_at":(self.created_at).strftime("%d-%m-%Y, %H:%M:%S")
        }

    @classmethod
    def getAllAircraftType(cls):
        return db.session.query(cls).filter(cls.is_deleted == 0).all()
