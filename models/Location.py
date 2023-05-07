from db import db
import datetime
from sqlalchemy import desc
from sqlalchemy import Column, DateTime
class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer,primary_key=True)
    parent_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(200))
    type = db.Column(db.String(150),default = "City")
    flag_file_id = db.Column(db.Integer, nullable=True)
    iso_code = db.Column(db.String(30),nullable=True)
    comment = db.Column(db.Text,nullable=True)
    is_deleted = db.Column(db.Integer,default=0)

    def json(self):
        return {
            "id":self.id,
            "parent_id":self.parent_id,
            "name":self.name,
            "type":self.type
        }

    @classmethod
    def getAllLocation(cls):
        return db.session.query(cls).filter(cls.is_deleted == 0).all()