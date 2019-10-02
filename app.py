#  Dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#  Database Setup

begin_date = dt.datetime(2017, 5, 1)
end_date = dt.datetime(2017, 5, 15)

engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect Database into ORM class
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement


# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route("/")
def hello_there():
    return (
        f"General Kenobi, here are your routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        # f"/api/v1.0/<start><br/>"
        # f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)

    results = session.query(Measurement).\
    filter(Measurement.date > begin_date - dt.timedelta(days=365)).filter(Measurement.date < end_date).all()

    session.close()

    all_data = []

    # Iterate through each row value in query 
    for row in results:
        
        # Make a dictionary for each row 
        prcp_dict = {}
        
        # Extract each column value per row of data
        prcp_dict["date"] = row.date
        prcp_dict["prcp"] = row.prcp
        
        # append row to list
        all_data.append(prcp_dict)

    return jsonify(all_data)



@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Measurement).group_by(Measurement.station).all()

    session.close()

    all_data = []

    for row in results:

        stations_dict = {}
        stations_dict["station"] = row.station

        all_data.append(stations_dict)

    return jsonify(all_data)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement).\
    filter(Measurement.date > begin_date - dt.timedelta(days=365)).filter(Measurement.date < end_date).all()

    session.close()

    all_data = []

    for row in results:

        tobs_dict = {}
        tobs_dict["date"] = row.date
        tobs_dict["tobs"] = row.tobs

        all_data.append(tobs_dict)

    return jsonify(all_data)


if __name__ == "__main__":
    app.run(debug=True)