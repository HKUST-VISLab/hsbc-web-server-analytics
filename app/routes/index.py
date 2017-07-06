# -*- coding: UTF-8 -*-
from app import app, mongo
import json
from flask import request

from app.DataService.DataService import DataService

data_service = DataService()
print('here')
@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/stationConfig')
def getStationConfig():
    """This is a function to return the station configuration data
    :return: the stationconfig file(json format)
    """
    data = data_service.get_stations()
    return json.dumps(data)




if __name__ == '__main__':
    with open('../../test_data/'+'full_station_config.json', 'r') as rf:
        windConstraint = json.load(rf)
        print('windConstrian', json.dumps(windConstraint))


