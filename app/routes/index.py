from app import app
import json

DATAPATH = 'test_data/'

@app.route('/stationConfig')
def getStationConfig():
    """This is a function to return the station configuration data

    :return: the stationconfig file(json format)
    """
    print('tesing')
    with open(DATAPATH+'full_station_config.json', 'r') as rf:
        stationConfig = json.load(rf)
    return json.dumps(stationConfig)

@app.route('/windConstraint')
def getWindConstraint():
    """ Temp and test function

    :return:,,,
    """
    with open(DATAPATH+'all_constraints_2.json', 'r') as rf:
        windConstraint = json.load(rf)
    return json.dumps(windConstraint)



