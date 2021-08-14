# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Dependencies for Flask
from flask import Flask, jsonify

# Engine t access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)

# ------------------------
# Set up Flask
# This will create a Flask application called "app."
app = Flask(__name__)

# define the welcome route 
@app.route("/")

# add the routing information with f strings
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Precipitation
@app.route("/api/v1.0/precipitation")

# create the precipitation() function
# This calculates the date one year ago from the most recent date in the database and then
# write a query to get the date and precipitation for the previous year adding also a filter
# use jsonify() to format our results into a JSON structured file
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Stations
@app.route("/api/v1.0/stations")

# Create the stations function
# Get all of the stations in our database
# unraveling our results into a one-dimensional array
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

