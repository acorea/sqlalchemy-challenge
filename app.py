import datetime as dt
from flask import Flask, redirect, render_template, jsonify
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<h3>Click on link below to get more weather info:</h3>
<ul>
    <li> <a href="/api/v1.0/precipitation">precipitation</a></li>
    <li> <a href="/api/v1.0/stations">stations</a></li>
    <li> <a href="/api/v1.0/tobs">tobs</a></li>
    <li> <a href="/api/v1.0/<start>">startDate</a></li>
    <li> <a href="/api/v1.0/<start>/<end>">endDate</a></li>
</ul>
'''
@app.route('/api/v1.0/precipitation')
def prcp():
    session = Session(engine)
    return { date:prcp for date, prcp in session.query(measurement.date, measurement.prcp) }

@app.route('/api/v1.0/stations')
def locale():
    session = Session(engine)
    return {  station:name for station, name  in session.query(station.station, station.name) }

@app.route('/api/v1.0/tobs')
def temps():
    session = Session(engine)
    return {  date:tobs for date, tobs  in session.query(measurement.date, measurement.tobs) }

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def ranges(start, end = '2017-08-23'):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).filter((measurement.date >= start) & (measurement.date <= end)).all()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)