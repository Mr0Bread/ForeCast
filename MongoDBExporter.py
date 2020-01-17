import pymongo
from Request import get_current_fill_data, get_past_fill_data, get_table


def get_station_names(fill_data: list) -> list:
    station_names = []

    for data_dict in fill_data:
        station_names.append(data_dict['Station'])

    return station_names


def get_scrape_time(data_dict: dict) -> str:
    return data_dict['Time']


class MongoDBExporter:
    def __init__(self):
        self.my_client = pymongo.MongoClient(
            "mongodb+srv://Mr0Bread:Elishka1Love@forecastcluster-ruxkg.gcp.mongodb.net/test?retryWrites=true&w=majority")
        self.database = self.my_client['MeteoInfoTable']

    def clear_collection(self, coll_name: str):
        self.database.drop_collection(coll_name)

    def clear_all_collections(self, coll_names: list):
        for name in coll_names:
            self.database.drop_collection(name)

    def get_collection(self, coll_name: str):
        return self.database[coll_name]

    def update_collection(self, coll_name: str, fill_data: dict):
        collection = self.get_collection(coll_name)
        collection.insert(fill_data)

    def delete_collection(self, coll_name: str):
        self.database[coll_name].drop()

    def get_collection_names(self) -> list:
        return self.database.list_collection_names()

    def fill_database(self, fill_data: list):
        for data_dict in fill_data:
            self.fill_collection(data_dict, data_dict['Station'])

    def fill_collection(self, data_dict: dict, coll_name: str):
        data_dict.pop('Station')

        collection = self.database[coll_name]
        collection.insert_one(data_dict)
