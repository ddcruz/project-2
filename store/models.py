from .app import db

class Store(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __repr__(self):
        return '<Store %r>' % (self.name)
