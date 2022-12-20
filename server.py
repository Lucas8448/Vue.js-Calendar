from flask import Flask, jsonify, session
from flask_cors import CORS, cross_origin
from collections import OrderedDict
import datetime
import sqlite3
import time
import json

# create database if it doesn't exist
conn = sqlite3.connect('db/days.db')
conn.execute('CREATE TABLE IF NOT EXISTS events (event_id INTEGER PRIMARY KEY AUTOINCREMENT, event_title TEXT, event_description TEXT, event_start INTEGER, event_end INTEGER, event_colour TEXT)')
conn.commit()
conn.close()


def get_week_dates(date):
    week = OrderedDict()
    date = datetime.datetime.strptime(date, '%d.%m.%Y')
    for i in range(7):
        day = date + datetime.timedelta(days=i)
        week[i] = {"name": day.strftime(
            "%A"), "date": day.strftime("%d.%m.%Y")}
    return week


def date_to_weekday(date):
    return time.strftime('%A', time.strptime(date, '%d.%m.%Y'))


DEBUG = True
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'


@app.route('/ping')
@cross_origin()
def ping():
    return jsonify('pong!')


@app.route('/goto/today')
@cross_origin()
def goto_today():
    week = get_week_dates(time.strftime('%d.%m.%Y'))
    return jsonify(
        {
            "day": time.strftime('%A'),
            "week": time.strftime('%W'),
            "date": time.strftime('%d.%m.%Y'),
            "weekNum": time.strftime('%W'),
            "week": week
        }
    )


@app.route('/goto/<date>')
@cross_origin()
def goto_date(date):
    return jsonify(
        {
            "day": time.strftime('%A', time.localtime(time.mktime(time.strptime(date, '%d.%m.%Y')))),
            "week": time.strftime('%W', time.localtime(time.mktime(time.strptime(date, '%d.%m.%Y')))),
            "date": time.strftime('%d.%m.%Y', time.localtime(time.mktime(time.strptime(date, '%d.%m.%Y')))),
            "weekNum": time.strftime('%W', time.localtime(time.mktime(time.strptime(date, '%d.%m.%Y')))),
            "week": get_week_dates(time.strftime('%d.%m.%Y', time.localtime(time.mktime(time.strptime(date, '%d.%m.%Y')))))
        }
    )


@app.route('/events/<date>')
@cross_origin()
def get_events(date):
    conn = sqlite3.connect('db/days.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE event_start <= ? AND event_end >= ?',
              (time.mktime(time.strptime(date, '%d.%m.%Y')), time.mktime(time.strptime(date, '%d.%m.%Y'))))
    events = c.fetchall()
    conn.close()
    return jsonify(events)


@app.route('/events/add/<title>/<description>/<start>/<end>')
@cross_origin()
def add_event(title, description, start, end):
    # convert YYYY-MM-DD to DD.MM.YYYY
    start = time.strftime('%d.%m.%Y', time.localtime(
        time.mktime(time.strptime(start, '%Y-%m-%d'))))
    end = time.strftime('%d.%m.%Y', time.localtime(
        time.mktime(time.strptime(end, '%Y-%m-%d'))))
    conn = sqlite3.connect('db/days.db')
    c = conn.cursor()
    colour = ""
    c.execute('INSERT INTO events (event_title, event_description, event_start, event_end, event_colour) VALUES (?, ?, ?, ?, ?)',
              (title, description, start, end, colour))
    conn.commit()
    conn.close()
    return jsonify(True)


if __name__ == '__main__':
    app.run(debug=True, port=5174)
