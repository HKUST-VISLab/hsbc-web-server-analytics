import json
import datetime
import pymongo
from pymongo import MongoClient
from app.DataService.Config import *
import time
from app.lib.lib import calc_pearsonr
from app.lib.lib import calc_rel_diff
from app.lib.lib import calc_abs_diff
# Warning: Should included into the config file

# Warning, all the collection should be read from the configure files

def calc_time(method):
    def serve(*args, **kargs):
        start_time = time.time()
        result = method(*args, **kargs)
        end_time = time.time()
        print('Run time of ' , method.__name__, 'is :', end_time - start_time)
        return result
    return serve

class DataService():
    """
    The function collection to query data from the Database
    """
    def __init__(self):
        # Warning, need to read from config
        self.__client = MongoClient(HOST, PORT)
        self.stations = self.__read_stations()

    def get_station(self):
        return self.__read_stations()


    @calc_time
    def __read_stations(self):
        """
        :return: list with  [{
        station code,
        station loc,
        station type}]
        """
        self.__station_db = self.__client[STATIONDB]
        self.weather_stations_collection = self.__station_db[WEATHERSTATIONCOLLECTION]
        self.aqi_stations_collection = self.__station_db[AQISTATIONCOLLECTION]

        station_list = []

        for station in self.weather_stations_collection.find():
            station_list.append({'station_code': station['station_code'],
                                 'loc': station['loc'],
                                 'type': 'weather'})


        for station in self.aqi_stations_collection.find():
            station_code = station['station_code']
            recent_record = self.get_recent_record(station_code)
            station_list.append({'station_code': station['station_code'],
                                 'loc': station['loc'],
                                 'recent': recent_record,
                                 'type': 'aqi'})


        return station_list

    def get_stations(self):
        return self.stations

    def aggregate_records(self):
        pass

    @calc_time
    def get_records_from_time_range(self, station_id = "CB_R", hour_range = 3, data_attr = "PM2_5", metric = "CorrCoefficient" , start_time = None, end_time = None):
        """

        :param station_id:
        :param start_time:
        :param end_time:
        :param range: aggregated range, unit: hour
        :return:
        """
        aqi_db = self.__client[AQIDB]
        # aqi_collection = aqi_db[AQICOLLECTION]
        aqi_collection = aqi_db['dev_aqi_prediction_aggregation_hkust']
        data_list = []
        previous_agg = None
        measure_diff = None
        if metric == "CorrCoefficient":
            measure_diff = calc_pearsonr
        elif metric == "RelError":
            measure_diff = calc_rel_diff
        elif metric == "AbsError":
            measure_diff = calc_abs_diff
        if start_time == None and end_time == None:
            for record in aqi_collection.find({'station_code': station_id}).sort('time', 1):
                current_agg = self.__generate_agg(record, data_attr, hour_range)
                sign, _agg = self.__merge_agg(previous_agg, current_agg)
                if sign == True:
                    previous_agg = _agg
                    data_list.append(_agg)


        for agg in data_list:
            aqi_values = agg['data']
            obs_values = [float(aqi_value[obs]) if aqi_value[obs] != None else None for aqi_value in aqi_values ]
            model_values = []
            for model in models:
                values = [float(aqi_value[model]) if aqi_value[model] != None else None for aqi_value in aqi_values]
                model_values.append(values)
                if "diff" not in agg:
                    agg["diff"] = {}
                r = list(measure_diff(obs_values, values))
                agg['diff'][model] = r
        for agg in data_list:
            if "struct_time" in agg:
                del agg["struct_time"]
        return data_list

    def get_recent_record(self, station_id="CB_R"):
        aqi_db = self.__client[AQIDB]
        aqi_collection = aqi_db[AQICOLLECTION]
        r_agg = aqi_collection.find({'station_code': station_id}).sort('time', pymongo.DESCENDING).limit(1)
        r_agg = list(r_agg)
        if len(r_agg) != 0:
            del r_agg[0]['_id']
            return r_agg[0]
        return None

    def __generate_agg(self, record, data_attr = "PM2_5", hour_range = 3):
        timestamp = record["time"]
        data = record[data_attr]
        struct_time = time.localtime(timestamp)
        return {
            "time": timestamp,
            "data": [data],
            "hour_range": hour_range,
            "struct_time": struct_time,
            "start_hour": int(struct_time.tm_hour / hour_range) * hour_range
        }

    def __merge_agg(self, preAgg, newAgg):
        """

        :param preAgg:
        :param newAgg:
        :param range:
        :return: sign, data:
            sign: True if a new aggregate is generated else False(the old aggregated is updated)
        """
        if preAgg == None:
            return True, newAgg

        if self.__same_day_and_hour(preAgg['struct_time'], newAgg['struct_time']) and preAgg["start_hour"] == newAgg["start_hour"]:
            preAgg["data"] += newAgg["data"]
            return False, preAgg

        del preAgg["struct_time"]
        return True, newAgg

    def __same_day_and_hour(self, struct_time1, struct_time2):
        return True if struct_time1.tm_year == struct_time2.tm_year \
                       and struct_time1.tm_mon == struct_time2.tm_mon \
                       and struct_time1.tm_mday == struct_time2.tm_mday \
            else False

# Warning: shoule be put into a lib module
def correct_time_format(time):
    if not isfloat(time):
        return False
    try:
        time = str(time)
    except ValueError as e:
        print('Error', e)

    if len(time) < 14:
        time = str(time)
        time += "0" * (14 - len(time))
    return time



# Warning: should be put into a lib module

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    data_service = DataService()
    station_records = data_service.get_recent_record()
    print(station_records)
    # result = data_service.get_records_from_time_range(hour_range=6)
    # import json
    # with open('data.json', 'w') as output:
    #     json.dump(result, output)
    # print(result)



