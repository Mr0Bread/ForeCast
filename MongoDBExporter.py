import pymongo
from Request import get_data_doc_from_data, get_data_from_old_tables, get_old_tables, get_modified_urls


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
        self.main_database = self.my_client['MeteoInfoTable']
        self.time_database = self.my_client['LastInsertTable']
        self.first_filling = True

    def clear_collection(self, coll_name: str):
        self.main_database.drop_collection(coll_name)

    def clear_all_collections(self, coll_names: list):
        for name in coll_names:
            self.main_database.drop_collection(name)

    def get_collection(self, coll_name: str):
        return self.main_database[coll_name]

    def update_collection(self, coll_name: str, fill_data: dict):
        collection = self.get_collection(coll_name)
        collection.insert(fill_data)

    def delete_collection(self, coll_name: str):
        self.main_database[coll_name].drop()

    def get_collection_names(self) -> list:
        return self.main_database.list_collection_names()

    def fill_database(self, fill_data: list):
        for data_dict in fill_data:
            self.fill_collection(data_dict, data_dict['Station'])

    def fill_collection(self, data_dict: dict, coll_name: str):
        data_dict.pop('Station')

        collection = self.main_database[coll_name]
        collection.insert_one(data_dict)

    def get_relevant_fill_data_doc(self, fill_data: list):
        for data_dict in fill_data:
            if not self.is_row_relevant(data_dict):
                fill_data.remove(data_dict)

        return fill_data

    def is_row_relevant(self, data_dict: dict):
        for data in data_dict:
            collection = self.time_database[data['Station']]
            selected_row = collection.find({}, {'_id': 0, 'Time': 1, 'Date': 1})

            if data['Time'] != selected_row['Time'] or data['Date'] != selected_row['Date']:
                return True
            else:
                return False

    def fill_time_database(self, fill_data: list):
        for data in fill_data:
            collection = self.time_database[data['Station']]
            collection.insert_one({'Time': data['Time'], 'Date': data['Date']})


exporter = MongoDBExporter()
exporter.fill_database(get_data_doc_from_data(get_data_from_old_tables(get_old_tables(get_modified_urls()))))
