import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement=Base.classes.measurement
station=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end> <br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of percipitation data per date"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    
    prcp_dict={date:prcp for date, prcp in resuts}

    return jsonify(prcp_dict)


    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stationes"""
    # Query all passengers
    results = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of percipitation data per date"""
    # Query all passengers
    results = session.query(measurement.date, measurement.tobs).all()
    
    last_year =dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    temp_data=session.query(measurement.date, measurement.tobs).filter(measurement.station=='USC00519281').\
    filter(measurement.date>=last_year).order_by(measurement.date.desc()).all()

    session.close()
    temp_data=list(np.ravel(temp_data))
    # Create a dictionary from the row data and append to a list
    
    # temp_date = []
    # for date, tobs in temp_data:
    #     temp_dict = {}
    #     temp_dict["date"] = date
    #     temp_dict["temperature"] = tobs
    #     temp_date.append(temp_dict)

    # return jsonify(temp_date)
    return jsonify(temp_data)

@app.route("/api/v1.0/temp/<start>")
def start_date(start=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results=session.query(func.min(measurement.tobs),
       func.max(measurement.tobs),
       func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    results_data=list(np.ravel(results))

    session.close()

    return jsonify(results_data)

@app.route("/api/v1.0/temp/<start>/<end>")
def end_date(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results=session.query(func.min(measurement.tobs),
       func.max(measurement.tobs),
       func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    results_data=list(np.ravel(results))

    session.close()

    return jsonify(results_data)

if __name__ == '__main__':
    app.run(debug=True)
