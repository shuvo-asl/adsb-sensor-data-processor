from db import db
from sqlalchemy import desc,Column,DateTime
from geoalchemy2 import Geometry
from geoalchemy2 import WKTElement
import datetime
class PositionHistory(db.Model):
    __tablename__ = 'position_histories'
    id = db.Column(db.Integer,primary_key=True)
    unique_code = db.Column(db.String(100))
    location = db.Column(Geometry(geometry_type='POINT', srid=4326))
    lat = db.Column(db.Float(precision=2))
    lon = db.Column(db.Float(precision=2))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=True)

    def __int__(self,unique_code,location,lat,lon,updated_at = None):
        self.unique_code = unique_code
        self.lat = lat
        self.lon = lon
        self.location = WKTElement(location,srid=4326)
        self.updated_at = updated_at

    def __str__(self):
        return self.unique_code
    def json(self):
        return {
            "id":self.id,
            "unique_code":self.unique_code,
            "lat":self.lat,
            "lon":self.lon,
            "location":str(self.location)
        }
    @classmethod
    def getAllPositionHistory(cls):
        return db.session.query(cls).all()
    @classmethod
    def getAllPositionHistoryByUniqueCode(cls,unique_code):
        return db.session.query(cls).filter(cls.unique_code==unique_code).all()
    def save(self):
        db.session.add(self);
        db.session.commit();