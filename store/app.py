# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)

from .models import City

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/city_data/<state_abbr>")
def cities(state_abbr):
    sel = [
        City.city
        , City.lat
        , City.lon
        , City.state
        , City.state_abbr
        , City.density
    ]

    results = db.session.query(*sel).filter(City.state_abbr == state_abbr).all()
    # print(results[0])
    
    city_data = [{
        "city": result[0]
        , "location": [result[1], result[2]]
        , "state": result[3]
        , "state_abbr": result[4]
        , "density": result[5]
    } for result in results]

    # print(city_data[0])
    return jsonify(city_data)

# if __name__ == "__main__":
app.run(debug=True)
