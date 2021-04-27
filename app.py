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
        f"____________________________________________________________________<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation <br/>"
        f" * The precipitation per dates<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f" * All the stations infomration<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f" * The temperatures from the last year for the most active station<br/>"
        f"<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f" * Put a date (YYYY-MM-DD) and it will return the min, max and average temperatures<br/>"
        f"<br/>"
        f"/api/v1.0/temp/<start>/<end> <br/>"
        f" * Put a start date (YYYY-MM-DD)  / end date (YYYY-MM-DD) and will return the min, max and average temperatures<br/>"
    )

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a list of percipitation data per date"""
    # Query the precipitation and date
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    
    prcp_dict={date:prcp for date, prcp in results}

    return jsonify(prcp_dict)

# Return a JSON list of stations from the dataset.
    
@app.route("/api/v1.0/stations")
def stations():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stationes"""
    # Query all stations by name
    results = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def temp():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a list of percipitation for the last year"""
    # Query all passengers
    results = session.query(measurement.date, measurement.tobs).all()
    
    # calclulating the last year from the most recent date
    last_year =dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    temp_data=session.query(measurement.date, measurement.tobs).filter(measurement.station=='USC00519281').\
    filter(measurement.date>=last_year).order_by(measurement.date.desc()).all()

    session.close()

    temp_data=list(np.ravel(temp_data))
    return jsonify(temp_data)

    # Another way is with a dictionary from the row data and append to a list
    # I've tried it as well and it looks good too.
    
    # temp_date = []
    # for date, tobs in temp_data:
    #     temp_dict = {}
    #     temp_dict["date"] = date
    #     temp_dict["temperature"] = tobs
    #     temp_date.append(temp_dict)

    # return jsonify(temp_date)
    

# Create a query to return the min, max and average temperatures for specific start date"

@app.route("/api/v1.0/temp/<start>")
def start_date(start=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    result_start=session.query(func.min(measurement.tobs),
       func.max(measurement.tobs),
       func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    result_start_data=list(np.ravel(result_start))

    session.close()

    return jsonify(result_start_data)

# Create a query to return the min, max and average temperatures for specific start and end date"

@app.route("/api/v1.0/temp/<start>/<end>")
def end_date(start=None, end=None):
    # Create a session (link) from Python to the DB
    session = Session(engine)
    results=session.query(func.min(measurement.tobs),
       func.max(measurement.tobs),
       func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    results_data=list(np.ravel(results))

    session.close()

    return jsonify(results_data)

if __name__ == '__main__':
    app.run(debug=True)
