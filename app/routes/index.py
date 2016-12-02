# -*- coding: UTF-8 -*-
from app import app, mongo
import json
from flask import request

from app.DB.DataService import data_service


@app.route('/')
def index():
    print('here')

    return app.send_static_file('index.html')


@app.route('/stationConfig')
def getStationConfig():
    """This is a function to return the station configuration data
    :return: the stationconfig file(json format)
    """
    return data_service.get_station_config()
@app.route('/getWeatherInTimeRange', methods=['POST'])
def getWeatherInTimeRange():
    post_data = json.loads(request.data.decode())
    start_time = None
    end_time = None
    start_time = post_data['start_time'] if 'start_time' in post_data else None
    end_time = post_data['end_time'] if 'end_time' in post_data else None

    if end_time != None and start_time!= None:
        return data_service.get_weather_by_range('current_weather', [start_time, end_time])

    return None

@app.route('/getRecentWeather', methods=['POST'])
def getCurrentWeather():
    return data_service.get_closed_records("current_weather")

@app.route('/getClosedWeather', methods=['POST'])
def getClosedWeather():
    post_data = json.loads(request.data.decode())
    time = post_data['time'] if 'time' in post_data else None
    if time != None:
        return data_service.get_closed_records()
    return None

@app.route('/windConstraint')
def getWindConstraint():
    """ Temp and test function
    :return:,,,
    """
    DATAPATH = "test_data/"
    with open(DATAPATH+'all_constraints_2.json', 'r') as rf:
        windConstraint = json.load(rf)
        print('windConstrian', windConstraint)
    return json.dumps(windConstraint)

if __name__ == '__main__':
    with open('../../test_data/'+'full_station_config.json', 'r') as rf:
        windConstraint = json.load(rf)
        print('windConstrian', json.dumps(windConstraint))


