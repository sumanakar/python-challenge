from datetime import datetime, timedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    filterdate = datetime.now() - timedelta(days=365)
    # Query all temp
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=filterdate).order_by(Measurement.date.desc()).all()
    all_prcp=[]

    for item in results:
        prcp_dict={}
        prcp_dict["date"]=item.date
        prcp_dict["prcp"]=item.prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    # Query all temp
    results = session.query(Station.station).distinct()
    all_station=[]
    for i in results:
        station_dict={}
        station_dict["station-name"]=i.station
        all_station.append(station_dict)
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query all temp
    filterdate = datetime.now() - timedelta(days=365)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=filterdate).order_by(Measurement.date.desc()).all()
    all_temp=[]

    for item in results:
        temp_dict={}
        temp_dict["date"]=item.date
        temp_dict["tobs"]=item.tobs
        all_temp.append(temp_dict)

    return jsonify(all_temp)


@app.route("/api/v1.0/<start>")
def start(start):

    stime=datetime.strptime(start,'%Y-%m-%d')
    
    # Query all temp

    max_result=session.query(func.max(Measurement.tobs)).filter(Measurement.date>=stime).first()
    min_result=session.query(func.min(Measurement.tobs)).filter(Measurement.date>=stime).first()
    avg_result=session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=stime).first()
    
    temp={}
    temp["Average Temp"]=avg_result[0]
    temp["Maximum Temp"]=max_result[0]
    temp["Minimum Temp"]=min_result[0]

    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    stime=datetime.strptime(start, '%Y-%m-%d')
    etime=datetime.strptime(end, '%Y-%m-%d')
    # Query all temp

    max_result=session.query(func.max(Measurement.tobs)).filter(Measurement.date>=stime).filter(Measurement.date<=etime).first()
    min_result=session.query(func.min(Measurement.tobs)).filter(Measurement.date>=stime).filter(Measurement.date<=etime).first()
    avg_result=session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=stime).filter(Measurement.date<=etime).first()
    
    temp={}
    temp["Average Temp"]=avg_result[0]
    temp["Maximum Temp"]=max_result[0]
    temp["Minimum Temp"]=min_result[0]

    return jsonify(temp)

if __name__ == '__main__':
    app.run(debug=True)