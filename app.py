# Import Flask libraries
from flask import Flask, jsonify

# Import sqlalchemy libraries
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import scipy
import numpy as np
import scipy.stats as st

# Import datetime
import datetime as dt

# Import directory pathing libraries
import os
import sys



print(os.path.dirname(__file__))

root_project_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, root_project_path)

hawaii_path = os.path.join(root_project_path, "Resources/hawaii.sqlite")

# Database Setup
engine = create_engine("sqlite:///"+hawaii_path)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Function to dynamically retrieve "one year ago" date
def last_date():
    # Query for last date
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Get last date as a datetime date object
    date_time_obj = dt.datetime.strptime(last_date.date, '%Y-%m-%d')
    # Parse out Y/M/D
    day_obj = date_time_obj.strftime("%d")
    mo_obj = date_time_obj.strftime("%m")
    # While parsing out Y, subtract 1 year
    year_obj = str(int(date_time_obj.strftime("%Y")) - 1)
    # Rebuild string to find "one year ago" date
    year_ago_str = f'{year_obj}-{mo_obj}-{day_obj}'
    session.close()
    return year_ago_str

# Flask Setup
# Create application
app = Flask(__name__)


# Homepage
@app.route("/")
def home_func():
    print(f'Server request received for homepage.')
    return (
    f'<br>Welcome to the Hawaii weather records database! <br><hr>'
    f'The following routes are available on this page: <br>'
    f'/api/v1.0/precipitation<br>'
    f'/api/v1.0/stations<br>'
    f'/api/v1.0/tobs <br><br>'
    f'*For the two routes below, please enter dates in the format of "YYYY-MM-DD"\
        for "&ltstart&gt" and "&ltend&gt" <br>'
    f'**Please enter only date ranges on or between 2010-01-01 to 2017-08-23<br>'
    f'/api/v1.0/&ltstart&gt <br>'
    f'/api/v1.0/&ltstart&gt/&ltend&gt <br>'
    )

# Precipitation page
@app.route(f'/api/v1.0/precipitation')
def prcp_func():
    print(f'Server request received for Precipitation page.')
    year_ago_var = last_date()
    session = Session(engine)
    last_12_mo = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago_var).all()
    session.close()
    last_12_mo_prcp = {}
    for date, prcp in last_12_mo:
        last_12_mo_prcp[date] = prcp
    return jsonify(last_12_mo_prcp)


# Stations page
@app.route(f'/api/v1.0/stations')
def stat_func():
    print(f'Server request received for Stations page.')
    session = Session(engine)
    all_stations = session.query(Station).all()
    session.close()
    stations_list = []
    for station_obj in all_stations:
        station_ind = {}
        station_ind["id"] = station_obj.id
        station_ind["station"] = station_obj.station
        station_ind["name"] = station_obj.name
        station_ind["latitude"] = station_obj.latitude
        station_ind["longitude"] = station_obj.longitude
        station_ind["elevation"] = station_obj.elevation
        stations_list.append(station_ind)
    return jsonify(stations_list)


# Temperature Observations page
@app.route(f'/api/v1.0/tobs')
def tobs_func():
    print(f'Server request received for Temperatore Observations page.')
    session = Session(engine)
    year_ago_var = last_date()
    station_active = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc()).first()
    active_station_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= year_ago_var)\
            .filter(Measurement.station == station_active[0]).all()
    active_station_dict = {}
    session.close()
    for date, tobs in active_station_data:
        active_station_dict[date] = tobs
    return jsonify(active_station_dict)



# JSON query page for historical-to-date information
@app.route("/api/v1.0/<start>")
def json_s_func(start):
    print(f'Server request received for start-only historical info page.')
    # Improvement: add an if statement checking formatting of the date string entered
    session = Session(engine)
    results_s = session.query(Measurement.tobs).filter(Measurement.date >= start)
    session.close()
    temp_list = [x.tobs for x in results_s]
    temp_min = st.tmin(temp_list)
    temp_avg = round(st.tmean(temp_list), 2)
    temp_max = st.tmax(temp_list)
    return (
        f'The temperature stats starting from {start} are:\
        Minimum: {temp_min}<br>\
        Average: {temp_avg}<br>\
        Maximum: {temp_max}'
    )



# JSON query page for specific time period
@app.route("/api/v1.0/<start>/<end>")
def json_se_func(start, end):
    print(f'Server request received for start-end historical info page.')
    # Improvement: add an if statement checking formatting of the date string entered
    session = Session(engine)
    results_s = session.query(Measurement.tobs).filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)
    session.close()
    temp_list = [x.tobs for x in results_s]
    temp_min = st.tmin(temp_list)
    temp_avg = round(st.tmean(temp_list), 2)
    temp_max = st.tmax(temp_list)
    return (
        f'The temperature stats from {start} to {end} are:<br>\
        Minimum: {temp_min}<br>\
        Average: {temp_avg}<br>\
        Maximum: {temp_max}'
        )


if __name__ == "__main__":
    app.run(debug=True)
