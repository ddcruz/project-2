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

    SQLStmt = """SELECT c.city, c.lat, c.lon, c.state, c.state_abbr, c.density, cd.population, cd.median_age, cd.average_household_size, cd.median_income FROM city c INNER JOIN city_demographics cd ON c.state_abbr = cd.state_abbr AND UPPER(c.city) = cd.city;"""
    print(SQLStmt)
    results = db.engine.execute(SQLStmt)
    print(results)
    city_data = [{
        "city": result[0]
        , "location": [result[1], result[2]]
        , "state": result[3]
        , "state_abbr": result[4]
        , "density": result[5]/2.56
        , "population": result[6]
        , "median_age": result[7]
        , "average_household_size": result[8]
        , "median_income": result[9]
    } for result in results]
    print(city_data)
    return jsonify(city_data)

@app.route("/api/demographics/<state_abbr>")
def city_demo(state_abbr):
    print(state_abbr)
    sel = [
        City_Demo.city
        , City_Demo.state
        , City_Demo.state_abbr
        , City_Demo.population
        , City_Demo.median_age
        , City_Demo.average_household_size
        , City_Demo.median_income
    ]

    results = db.session.query(*sel).filter(City_Demo.state_abbr == state_abbr).all()

    print(results)
    city_demographics = [{
        'city': result.city
        , 'state': result.state
        , "state_abbr": result.state_abbr
        , "population": result.population
        , "median_age": result.median_age
        , "median_income": result.median_income
    } for result in results]

    print(city_demographics)
    return jsonify(city_demographics)

# @app.route("/api/demographics/<state_abbr>")
# def state_demo(state_abbr):
#     sel = [
#         State_Demo.city
#         , State_Demo.state
#         , State_Demo.state_abbr
#         , State_Demo.population
#         , State_Demo.median_age
#         , State_Demo.average_household_size
#         , State_Demo.median_income
#         , State_Demo.household_income
#         , State_Demo.per_capita_income
#     ]
#     results = db.session.query(*sel).filter(State_Demo.state_abbr == state_abbr).all()

#     state_demographics = {
#         "state": results[0][1],
#         # "state_abbr": results[0][2],
#         "population": results[0][3],
#         "median_age": results[0][4],
#         "avgerage_household_size": results[0][5],
#         "median_income": results[0][6],
#         "household_income": results[0][7],
#         "per_capita_income": results[0][8]
#     }

#     return jsonify(state_demographics)


@app.route("/api/plot/<state_abbr>")
def plot(state_abbr):
    sel = [
        City_Demo.city
        , City_Demo.state_abbr
        , City_Demo.median_age
        , City_Demo.median_income
    ]
    results = db.session.query(*sel).filter(City_Demo.state_abbr == state_abbr).all()
    
    cities = []
    med_age = []
    med_income = []

    for city in results:
        cities.append(city[0])
        med_age.append(city[2])
        med_income.append(city[3])

    results_json = {
        "cities": cities,
        "med_age": med_age,
        "med_income": med_income
     }

    return jsonify(results_json)


@app.route("/api/pie/<state_abbr>")
def pie(state_abbr):
    # print(state_abbr)
    sel = [
        City.city
        , City.state_abbr
        , City.density
    ]
    results = db.session.query(*sel).filter(City.state_abbr == state_abbr).order_by(City.density.desc()).all()

    top_10 = results[0:10]

    cities = []
    density = []
     
    for city in top_10:
        cities.append(city[0])
        density.append(city[2]/2.56)

    results_json = {
        "cities": cities,
        "density": density,
     }

    print(results_json)
    return jsonify(results_json)

# if __name__ == "__main__":
app.run(debug=True)
