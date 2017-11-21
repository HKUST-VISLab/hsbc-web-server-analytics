# -*- coding: UTF-8 -*-
from app import app, mongo
import json
from flask import request
from flask import send_file
from app.DataService.DataService import DataService
import os.path

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


@app.route('/getallrecordsofstation', methods=['POST'])
def getRecordOfStations():

    post_data = json.loads(request.data.decode())
    station_id = post_data['stationId']
    start_time = post_data['start_time']
    end_time = post_data['end_time']
    aqi_attr = post_data['attr']
    hour_range = post_data['hour_range']
    metric = post_data['metric']
    print('query', station_id, hour_range, metric, aqi_attr, start_time, end_time)
    query_result = data_service.get_records_from_time_range(
        station_id=station_id,
        start_time=start_time,
        end_time=end_time,
        data_attr=aqi_attr,
        hour_range=hour_range,
        metric=metric
    )
    return json.dumps(query_result)


@app.route('/get_aq_station_img', methods=['GET', 'POST'])
def getImages():
    station_code = request.args.get('station_code')
    img_name = 'aq_' + station_code + '.jpg'
    current_path = os.path.dirname(os.path.abspath(__file__))
    img_folder = os.path.join(current_path, '../../img')
    file_path = os.path.join(img_folder, img_name)

    print('getImages',file_path, os.path.isfile(file_path) )

    if os.path.isfile(file_path) == False:
        file_path = '../img/' + 'not_found' + '.jpg'

    return send_file(file_path, mimetype='image/gif')


if __name__ == '__main__':
    with open('../../test_data/'+'full_station_config.json', 'r') as rf:
        windConstraint = json.load(rf)
        print('windConstrian', json.dumps(windConstraint))


