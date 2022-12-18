from flask import Flask, jsonify, session
from flask_cors import CORS, cross_origin
import sqlite3
import time

# create database if it doesn't exist
conn = sqlite3.connect('db/days.db')
conn.execute('CREATE TABLE IF NOT EXISTS events (event_id INTEGER PRIMARY KEY AUTOINCREMENT, event_title TEXT, event_description TEXT, event_start INTEGER, event_end INTEGER, event_colour TEXT)')
conn.commit()
conn.close()


def date_to_weekday(date):
    return time.strftime('%A', time.strptime(date, '%Y-%m-%d'))


DEBUG = True
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'


@app.route('/ping')
@cross_origin()
def ping():
    return jsonify('pong!')


@app.route('/get/week')
@cross_origin()
def get_week():
    return jsonify(time.strftime('%W'))


@app.route('/get/day')
@cross_origin()
def get_day():
    return jsonify(time.strftime('%A'))

@app.route('/day/<week>/<day>')
@cross_origin()
def day(week, day):
    return jsonify(date_to_weekday('2020-W' + week + '-' + day))

if __name__ == '__main__':
    app.run(debug=True)
