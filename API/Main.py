from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps, dump
from flask_jsonpify import jsonify
from Program.MongoDBClient import MongoDBClient
from Program.DataHandler import DataHandler

app = Flask(__name__)
api = Api(app)

db_client = MongoDBClient('MeteoInfoTable2', 'LastInsertTable2')


@app.route('/get/', methods=['GET'])
def example():
    for x in request.args.keys():
        if x == 'value' and request.args['value'] != 'Station':
            return DataHandler.get_json(
                DataHandler.get_lists_of_chosen_values(db_client.get_info_from_main_database(), request.args['value']))
        elif x == 'list' and request.args['list'] == 'all':
            return DataHandler.get_json_of_existing_values()
        elif (x == 'value' and request.args['value'] == 'Station') or (x == 'list' and request.args['list'] == 'Station'):
            return DataHandler.get_json_of_station_names()


app.run(port='5001', debug=True)
