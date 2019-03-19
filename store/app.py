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

from .models import City, City_Demo, State_Demo

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/city_list/<state_abbr>')
def cities(state_abbr):
    sel = [
        City_Demo.city
    ]

    results = db.session.query(*sel).filter(City_Demo.state_abbr == state_abbr).all()

    city_data = [{
        "city": result[0]
        } for result in results
    ]

    return jsonify(city_data)

@app.route("/api/city_data/<state_abbr>")
def density_by_city_by_state(state_abbr):
    sel = [
        City.city
        , City.lat
        , City.lon
        , City.state
        , City.state_abbr
        , City.density
    ]

    results = db.session.query(*sel).filter(City.state_abbr == state_abbr).all()
    
    city_data = [{
        "city": result[0]
        , "location": [result[1], result[2]]
        , "state": result[3]
        , "state_abbr": result[4]
        , "density": result[5]
    } for result in results]

    return jsonify(city_data)

@app.route("/api/demographics/<state_abbr>/<city>")
def city_demo(state_abbr, city):
    sel = [
        City_Demo.city
        , City_Demo.state
        , City_Demo.state_abbr
        , City_Demo.population
        , City_Demo.median_age
        , City_Demo.average_household_size
        , City_Demo.median_income
        , City_Demo.household_income
        , City_Demo.per_capita_income
    ]

    results = db.session.query(*sel).filter(City_Demo.state_abbr == state_abbr).filter(City_Demo.city == city).all()
    # print(results)
    city_demographics = {
        "city": results[0][0],
        "state": results[0][1],
        # "state_abbr": results[0][2],
        "population": results[0][3],
        "median_age": results[0][4],
        "avgerage_household_size": results[0][5],
        "median_income": results[0][6],
        "household_income": results[0][7],
        "per_capita_income": results[0][8]
    }
    # print(city_demographics)
    return jsonify(city_demographics)

@app.route("/api/demographics/<state_abbr>")
def state_demo(state_abbr):
    sel = [
        State_Demo.city
        , State_Demo.state
        , State_Demo.state_abbr
        , State_Demo.population
        , State_Demo.median_age
        , State_Demo.average_household_size
        , State_Demo.median_income
        , State_Demo.household_income
        , State_Demo.per_capita_income
    ]
    results = db.session.query(*sel).filter(State_Demo.state_abbr == state_abbr).all()

    state_demographics = {
        "state": results[0][1],
        # "state_abbr": results[0][2],
        "population": results[0][3],
        "median_age": results[0][4],
        "avgerage_household_size": results[0][5],
        "median_income": results[0][6],
        "household_income": results[0][7],
        "per_capita_income": results[0][8]
    }

    return jsonify(state_demographics)

# if __name__ == "__main__":
app.run(debug=True)
