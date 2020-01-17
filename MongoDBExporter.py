import pymongo
from Request import get_data_doc

my_client = pymongo.MongoClient(
    "mongodb+srv://Mr0Bread:Elishka1Love@forecastcluster-ruxkg.gcp.mongodb.net/test?retryWrites=true&w=majority")

database = my_client['MeteoInfoTable']

my_dict = get_data_doc()
