from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from Program.MongoDBClient import MongoDBClient
from Program.DataHandler import DataHandler

app = Flask(__name__)
api = Api(app)

db_client = MongoDBClient('MeteoInfoTable2', 'LastInsertTable2')


class DewPoint(Resource):
    @staticmethod
    def get():
        return DataHandler.get_lists_of_chosen_values(db_client.get_info_from_main_database(), 'Dew Point')


api.add_resource(DewPoint, '/dewpoint')
app.run(host='0.0.0.0')
