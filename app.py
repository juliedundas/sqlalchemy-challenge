# 1. Import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#Database setup

#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################

# 2. Flask setup
app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    #print(recent_date[0])

    # Calculate the date 1 year ago from the last data point in the database
    one_year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > one_year_prior).\
    order_by(Measurement.date).all()

    #Save results into dictionary
    prcp_dict = dict(precipitation_data)

    return jsonify(prcp_dict)



@app.route("/api/v1.0/stations")
def stations():
    # Design a query to show how many stations are available in this dataset?
    station_count = engine.execute("SELECT COUNT(station) FROM station")
    # List the stations and the counts in descending order.
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(Measurement.station.desc()).all()

    #Save results into json list
    return jsonify(active_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the last 12 months of temperature observation data for this station
    one_year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temperature_observations = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_prior).all()

    #Convert results into list
    temp_list = list(temperature_observations)

    return jsonify(temp_list)


@app.route("/api/v1.0/<start>")
def hello(start):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date =  dt.date(2012, 3, 25)
    starts = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return jsonify(starts)

@app.route("/api/v1.0/<start>/<end>")
def range(start_date, end_date):

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    mytime = "2012-03-25"
    end_date =  dt.date(mytime, '%Y-%m-%d')
    range_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.date).all()
    range_dates_listed =list(between_dates)


    return jsonify(range_dates_listed)


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
