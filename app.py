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
    <h1>Welcome to the Climate Analysis API!</h1>
    <h2>Available Routes:</h2>
    <ul>
    <li><a href="/api/v1.0/precipitation">Precipitation</a></li> 
    <li><a href="/api/v1.0/stations">Stations</a></li>
    <li><a href="/api/v1.0/tobs">Tobs</a></li>
    <li><a href="/api/v1.0/temp/2017-06-01/2017-06-31"> Add 2017-06-01/2017-06-31</a></li>
    </ul>
    ''')

# Precipitation
@app.route("/api/v1.0/precipitation")

# create the precipitation() function
# This calculates the date one year ago from the most recent date in the database and then
# write a query to get the date and precipitation for the previous year adding also a filter
# use jsonify() to format our results into a JSON structured file
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
   session.close()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Stations
@app.route("/api/v1.0/stations")

# Create the stations function
# Get all of the stations in our database
# unraveling our results into a one-dimensional array
def stations():
    results = session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Temperature
@app.route("/api/v1.0/tobs")

# Temperature function
# Calculate the date one year ago from the last date in the database.
# query the primary station for all the temperature observations from the previous year
# unravel the results into a one-dimensional array and convert that array into a list
# jsonify our temps list, and then return it
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# report on the minimum, average, and maximum temperatures
# provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>") 

# Statistics
# start and end parameters
# create a query with the func. min avg and max
# Create a list called sel
# Determine the starting and ending date
# We'll need to query our database using the list that we just made.
# Then, we'll unravel the results into a one-dimensional array and convert them to a list.
# Finally, we will jsonify our results and return them
# the asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
# get our statistics data
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel
        ).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).filter(Measurement.date >= start
    ).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run()