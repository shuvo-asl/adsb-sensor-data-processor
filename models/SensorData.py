from db import db
from sqlalchemy import JSON

class SensorData(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(JSON,nullable=True)

    def __int__(self,data):
        self.data  = data

    def json(self):
        return {
            "id":self.id,
            "data":self.data
        }

    @classmethod
    def getAllAircrafts(cls):
        return db.session.query(cls).limit(50).all()
    def save(self):
        db.session.add(self)
        db.session.commit()