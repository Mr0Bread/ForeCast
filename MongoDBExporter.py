import pymongo
from Request import get_data_doc


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

    def fill_collection(self, coll_name: str, fill_data: list):
        collection = self.get_collection(coll_name)
        collection.insert()
