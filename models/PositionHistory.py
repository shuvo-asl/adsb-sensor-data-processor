from db import db
from sqlalchemy import desc
from geoalchemy2 import Geometry
from geoalchemy2 import WKTElement
class PositionHistory(db.Model):
    __tablename__ = 'position_histories'
    id = db.Column(db.Integer,primary_key=True)
    unique_code = db.Column(db.String(100))
    location = db.Column(Geometry(geometry_type='POINT', srid=4326))

    def __int__(self,unique_code,location):
        self.unique_code = unique_code
        self.location = WKTElement(location,srid=4326)

    def json(self):
        return {
            "id":self.id,
            "unique_code":self.unique_code,
            "location":self.location
        }
    @classmethod
    def getAllPositionHistory(cls):
        return db.session.query(cls).all()
    def save(self):
        db.session.add(self);
        db.session.commit();