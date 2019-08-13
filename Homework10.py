#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 22:17:02 2019

@author: chrismiller
"""

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd
import datetime as dt
import flask as flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#####################################
app = Flask(__name__)


#main page
@app.route("/")
def welcome():
    return (
        f"Welcome to the my flask!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.  
@app.route("/api/v1.0/precipitation")
def jsonify():
    
    
     # Create our session (link) from Python to the DB   
    session = Session(engine)
    
    # find the date one year ago
    Last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    Year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)   
    
    #perform the query
    sel = [Measurement.date,func.avg(Measurement.prcp)]
    daily_averages = session.query(*sel).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-24').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()   
    session.close()

    #set the dateframe and indesx
    df = pd.DataFrame(daily_averages, columns=['date', 'precip'])
    df.set_index("date", inplace = True)

    #convert to dictionary
    dictionary = df.to_dict(orient="date")
    return dictionary


#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Station.name).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for stations in results:
        station_dict = {}
        station_dict["name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)


#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(hello_dict)

def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query the tobs data within the desired dates
    sel = [Measurement.date, func.avg(Measurement.tobs)]
    daily_averages = session.query(*sel).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-24').\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    session.close()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_dates = []
    for days in daily_averages:
        tobs_dict = {}
        tobs_dict["Temperature Observation"] = tobs
        all_dates.append(tobs_dict)

    return jsonify(all_dates)

if __name__ == "__main__":
    app.run(debug=True)
    
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given 
#start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#@app.route("/api/v1.0/<start>")
           
#@app.route("/api/v1.0/<start>/<end>")