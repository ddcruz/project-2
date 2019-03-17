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

class City_Demo(db.Model):
    __tablename__ = 'city_demographics'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    state_abbr = db.Column(db.String(64))
    population = db.Column(db.Float)
    median_age = db.Column(db.Float)
    average_household_size = db.Column(db.Float)
    median_income = db.Column(db.Float)
    household_income = db.Column(db.Float)
    per_capita_income = db.Column(db.Float)


    def __repr__(self):
        return '<City_Demo %r>' % (self.name)

class State_Demo(db.Model):
    __tablename__ = 'state_demographics'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(64))
    population = db.Column(db.Float)
    median_age = db.Column(db.Float)
    average_household_size = db.Column(db.Float)
    median_income = db.Column(db.Float)
    household_income = db.Column(db.Float)
    per_capita_income = db.Column(db.Float)

    def __repr__(self):
        return '<State_Demo %r>' % (self.name) 