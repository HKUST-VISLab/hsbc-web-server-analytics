import json
import datetime
from pymongo import MongoClient

# Warning: Should included into the config file
HOST = "127.0.0.1"
PORT = 27017
DB = "hk_weather_data"
# Warning, all the collection should be read from the configure files


class DataService():
    """
    The function collection to query data from the Database
    """
    def __init__(self):
        # Warning, need to read from config
        self.__client = MongoClient(HOST, PORT)
        self.__db = self.__client[DB]


    def get_station_config(self):
        """
        Read the configuration of stations from the database and return as the json format
        :return:{"Stations":[]}
        """
        collection = self.__db['station']
        station_config = []
        for record in collection.find():

            single_station = {}
            for _attr in record:
                if _attr == '_id':
                    continue
                single_station[_attr] = record[_attr]
            station_config.append(single_station)

        return json.dumps({
            'Stations': station_config
        })

    def get_weather_by_range(self, collection_name, time_range, time_attr="time"):
        """
        This function get the historical weather records in the time_range

        :param collection_name: the name of the collection
        :param time_range: an array with two elements[start_time, end_time]. start_time and end_time: yyyyMMddhhmmss
        :param time_attr: the attributes which record time
        :return: {time1: [], time2: []}
        """
        [start_time, end_time] = time_range
        start_time = correct_time_format(start_time)
        end_time = correct_time_format(end_time)
        if start_time == False and end_time == False:
            print('Time format is incorrect!')
            return {}

        # Warning should be revised by unifying all the time format
        if (collection_name == "forecast_weather"):
            start_time = int(start_time)
            end_time = int(end_time)
        # End warning

        weather_collection = self.__db[collection_name]

        time_range_query = {time_attr: {
            "$gte": start_time,
            "$lte": end_time
        }}

        time_2_weather_record = dict()

        for record in weather_collection.find(time_range_query):

            # Deal with  _id problem(from mongodb)
            if '_id' in record:
                del record['_id']

            # Find records of time
            if 'time' not in record:
                print('No time in this record!')
                continue
            time = correct_time_format(record['time'])
            if time == False:
                print('Error time format!')
                continue
            # Assign record to the specific time
            if time not in time_2_weather_record:
                time_2_weather_record[time] = []

            time_2_weather_record[time].append(record)


        return json.dumps(time_2_weather_record)

    def find_closed_records(self, collection_name, time, time_attr='time'):
        """
        This function get the closed records of time

        :param collection_name: the name of the collection
        :param time: the time to be considered
        :param time_attr: the attributes which record time
        :return: {time: time, records:[]}
        """
        time = correct_time_format(time)
        if time == False:
            print('Time format is incorrect!')
            return {}

        #  Warning should be revised by unifying all the time format
        if(collection_name == "forecast_weather"):
            time = int(time)
        # End warning

        weather_collection = self.__db[collection_name]
        closest_below_records = weather_collection.find({"time": {"$lte": time}}).sort(time_attr, -1)

        records = []
        closest_time = None
        for record in closest_below_records:
            if closest_time == None:
                closest_time = record[time_attr]
            if "_id" in record:
                del record['_id']
            if closest_time == record[time_attr]:
                records.append(record)
            else:
                return json.dumps({
                    'time': closest_time,
                    'records': records
                })

        print('To the start!')
        return {}

    def find_recent_records(self, collection_name):
        """
        This function get the latest records in the collection
        :param collection_name: the name of the collection
        :return:same as the "find_closed_records"
        """
        now_time = datetime.datetime.now()
        query_time_string = now_time.strftime("%Y%m%d%H%M%S")
        return self.find_closed_records(collection_name, query_time_string)


# Warning: shoule be put into a lib module
def correct_time_format(time):
    if not isfloat(time) :
        return False
    try:
        time = str(time)
    except ValueError as e:
        print('Error', e)

    if len(time) < 14:
        time = str(time)
        time += "0" * (14 - len(time))
        return time



# Warning: shoule be put into a lib module

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

data_service = DataService()


if __name__ == '__main__':
    data_service = DataService()
    start_time = '201611101829'
    end_time =   '201611152215'
    # current_weather forecast_weather
    # result = data_service.find_closed_records('forecast_weather',"201611302215")
    # print(data_service.find_recent_records('current_weather'))
    print(data_service.get_weather_by_range('forecast_weather', [start_time, end_time]))
    # print(result)
    # data_service.get_recent_weather([start_time, end_time])
