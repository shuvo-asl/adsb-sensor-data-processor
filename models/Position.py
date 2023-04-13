from db import db

class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer,primary_key=True)
    unique_code = db.Column(db.String(100))
    lat = db.Column(db.Float(precision=2))
    lon = db.Column(db.Float(precision=2))
    alt = db.Column(db.Float(precision=2))

    def __int__(self,unique_code,lat,lon,alt):
        self.unique_code = unique_code
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def json(self):
        {
            "id":self.id,
            "unique_code":self.unique_code,
            "lat":self.lat,
            'lon':self.lon,
            "alt":self.alt
        }
    @classmethod
    def getPositionByUniqueCode(cls,code):
        return db.session.query(cls).filter(cls.unique_code == code).first()
    def save(self):
        db.session.add(self);
        db.session.commit();