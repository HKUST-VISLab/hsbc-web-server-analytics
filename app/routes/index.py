# -*- coding: UTF-8 -*-
from app import app, mongo
import json

from app.DB.DataService import data_service

DATAPATH = 'test_data/'

@app.route('/')
def index():
    print('here')

    return app.send_static_file('index.html')


@app.route('/stationConfig')
def getStationConfig():
    """This is a function to return the station configuration data

    :return: the stationconfig file(json format)
    """
    #  Warning: This line should be packaged
    # return get_station_config()
    return data_service.get_station_config()
@app.route('/windConstraint')
def getWindConstraint():
    """ Temp and test function

    :return:,,,
    """
    with open(DATAPATH+'all_constraints_2.json', 'r') as rf:
        windConstraint = json.load(rf)
        print('windConstrian', windConstraint)
    return json.dumps(windConstraint)

if __name__ == '__main__':
    with open('../../test_data/'+'full_station_config.json', 'r') as rf:
        windConstraint = json.load(rf)
        print('windConstrian', json.dumps(windConstraint))


