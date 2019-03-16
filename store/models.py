from .app import db

class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))
    state_abbr = db.Column(db.String(2))
    state = db.Column(db.String(64))
    county = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    density = db.Column(db.Float)

    def __repr__(self):
        return '<City %r>' % (self.name)
