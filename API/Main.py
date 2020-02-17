from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps, dump
from flask_jsonpify import jsonify
from Program.MongoDBClient import MongoDBClient
from Program.DataHandler import DataHandler
from Program.KalmanFilter import KalmanFilter

app = Flask(__name__)
api = Api(app)

db_client = MongoDBClient('MeteoInfoTable2', 'LastInsertTable2')


@app.route('/get/', methods=['GET'])
def get_basic():
    for x in request.args.keys():
        if x == 'value' and request.args['value'] != 'Station':
            return DataHandler.get_json(
                DataHandler.get_lists_of_chosen_values_with_station_names(db_client.get_info_from_main_database(), request.args['value']))
        elif x == 'list' and request.args['list'] == 'all':
            return DataHandler.get_json_of_existing_values()
        elif (x == 'value' and request.args['value'] == 'Station') or (
                x == 'list' and request.args['list'] == 'Station'):
            return DataHandler.get_json_of_station_names()


@app.route('/get/estimations/', methods=['GET'])
def get_estimations():
    for x in request.args.keys():
        if x == 'value':

            error_in_estimate: float = request.args['err_in_est']
            error_in_measurement: float = request.args['err_in_meas']
            value_to_estimate: str = request.args['value']
            lists_of_estimates = []

            lists_of_measurements, station_names = DataHandler.get_prepared_lists_for_estimation(
                db_client.get_info_from_main_database(), value_to_estimate)

            for measurements in lists_of_measurements:
                initial_estimate = KalmanFilter.get_initial_estimate_based_on_last_measurements(measurements)
                kf = KalmanFilter(error_in_estimate, initial_estimate, error_in_measurement, measurements)
                lists_of_estimates.append(kf.get_list_of_estimates())

            accuracies = DataHandler.get_estimation_accuracy(lists_of_estimates, lists_of_measurements, station_names)


app.run(port='5001', debug=True)
