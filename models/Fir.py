from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
class Fir(db.Model):
    __tablename__ = 'fir'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, index=True)
    latitude = db.Column(db.String(255), nullable=True, index=False)
    longitude = db.Column(db.String(255), nullable=True, index=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)


    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "created_at":(self.created_at).strftime("%d-%m-%Y, %H:%M:%S")
        }

    @classmethod
    def getAllFirs(cls):
        return db.session.query(cls).filter(cls.is_deleted == 0).all()

