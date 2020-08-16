import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify,json


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    precip= session.query(measurement.date,measurement.prcp).filter(measurement.date>='2016-08-23').\
        filter(measurement.prcp).all()
    

    session.close()

    # Convert list of tuples into normal list
    precip_list = list(np.ravel(precip))
    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations=session.query(measurement.station).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    
    session.close()
    # Convert list of tuples into normal list
    stations_list= list(np.ravel(stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    top= session.query(measurement.date,measurement.tobs).filter(measurement.date>='2016-08-23').\
    filter(measurement.prcp).\
    filter(measurement.station=='USC00519281').\
    order_by(measurement.tobs.desc()).all()
 
    session.close()
    # Convert list of tuples into normal list
    tobs_list= list(np.ravel(top))
    return jsonify(tobs_list)

if __name__ == "__main__":
    app.run(debug=True)