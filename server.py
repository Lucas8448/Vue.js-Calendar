from flask import Flask, jsonify, session
from flask_cors import CORS, cross_origin
import sqlite3
import time
import json
import pytz
import datetime

def get_time_zone(country_code):
    # Get a list of all time zones
    time_zones = pytz.all_timezones
    # Iterate through the list of time zones
    for time_zone in time_zones:
        # Split the time zone into its components (e.g. "Europe/Paris" -> ("Europe", "Paris"))
        tz_components = time_zone.split('/')
        # If the first component (the continent) matches the country code, return the time zone
        if tz_components[0] == country_code:
            return time_zone
    # If no matching time zone was found, return None
    return None

def get_dates_of_week():
    # Get the current date
    now = datetime.datetime.now()

    # Set the day of the week to Monday (0)
    now = now - datetime.timedelta(days=now.weekday())

    # Initialize a list to hold the dates
    dates = []

    # Iterate through the days of the week
    for i in range(7):
        # Append the date to the list
        dates.append(now.date())
        # Increment the date by one day
        now += datetime.timedelta(days=1)

    # Return the list of dates
    return dates

# create database if it doesn't exist
conn = sqlite3.connect('db/days.db')
conn.execute('CREATE TABLE IF NOT EXISTS events (event_id INTEGER PRIMARY KEY AUTOINCREMENT, event_title TEXT, event_description TEXT, event_start INTEGER, event_end INTEGER, event_colour TEXT)')
conn.commit()
conn.close()


def date_to_weekday(date):
    return time.strftime('%A', time.strptime(date,  '%d.%m.%Y'))


DEBUG = True
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'


@app.route('/ping')
@cross_origin()
def ping():
    return jsonify('pong!')

@app.route('/today')
@cross_origin()
def get_today():
    return jsonify({
        "date": time.strftime('%d.%m.%Y'),
        "datetime": time.time(),
        "days": json.dumps(get_dates_of_week()),
        "weekday": time.strftime('%A'),
        "week": time.strftime('%W'),
        "month": time.strftime('%B'),
        "year": time.strftime('%Y'),
        "timezone": time.strftime('%Z')
        })

@app.route('/goto/date/<date>')
@cross_origin()
def get_date(date):
    return jsonify({"date": date, "weekday": date_to_weekday(date), "week": time.strftime('%W', time.strptime(date, '%d.%m.%Y')), "month": time.strftime('%B', time.strptime(date, '%d.%m.%Y')), "year": time.strftime('%Y', time.strptime(date, '%d.%m.%Y'))})

@app.route('/goto/day/<day>/<date>')
@cross_origin()
def get_day(day, date):
    return jsonify({"date": time.strftime('%d.%m.%Y', time.strptime(date, '%d.%m.%Y') + time.timedelta(days=int(day))), "weekday": date_to_weekday(time.strftime('%d.%m.%Y', time.strptime(date, '%d.%m.%Y') + time.timedelta(days=int(day)))), "week": time.strftime('%W', time.strptime(date, '%d.%m.%Y') + time.timedelta(days=int(day))), "month": time.strftime('%B', time.strptime(date, '%d.%m.%Y') + time.timedelta(days=int(day))), "year": time.strftime('%Y', time.strptime(date, '%d.%m.%Y') + time.timedelta(days=int(day)))})

@app.route('/goto/week/<week>')
@cross_origin()
def get_week(week):
    return jsonify({"date": time.strftime('%d.%m.%Y', time.strptime(week, '%W')), "weekday": date_to_weekday(time.strftime('%d.%m.%Y', time.strptime(week, '%W'))), "week": week, "month": time.strftime('%B', time.strptime(week, '%W')), "year": time.strftime('%Y', time.strptime(week, '%W'))})

    
if __name__ == '__main__':
    app.run(debug=True, port=5174)
