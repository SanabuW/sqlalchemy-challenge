from flask import Flask
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
    f'/api/v1.0/&ltstart&gt <br>'
    f'/api/v1.0/&ltstart&gt/&ltend&gt <br>'
    )

# Precipitation page
@app.route("/api/v1.0/precipitation")
def prcp_func():
    print("[printMessage]")
    return "[returnMessage]"


# Stations page
@app.route("/api/v1.0/stations")
def stat_func():
    print("[printMessage]")
    return "[returnMessage]"


# Temperature Observations page
@app.route("/api/v1.0/tobs")
def tobs_func():
    print("[printMessage]")
    return "[returnMessage]"



# JSON query page for historical-to-date information
@app.route("/api/v1.0/<start>")
def json_s_func():
    print("[printMessage]")
    return "[returnMessage]"



# JSON query page for specific time period
@app.route("/api/v1.0/<start>/<end>")
def json_se_func():
    print("[printMessage]")
    return "[returnMessage]"


if __name__ == "__main__":
    app.run(debug=True)
