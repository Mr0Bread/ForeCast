from Program.DataHandler import DataHandler
from Program.KalmanFilter import KalmanFilter
from Program.AutoDBFiller import AutoDBFiller
from Program.GraphEditor import GraphEditor
from Program.FileHandler import FileHandler
from Program.MySQLClient import MySQLClient
from Program.MongoDBClient import MongoDBClient
from Program.Request import Request
from matplotlib import pyplot as plt
from openpyxl import Workbook
import numpy as np

if __name__ == '__main__':
    sql_client = MySQLClient('139.59.212.33', 'outsider', 'password', 'forecast')

    value = 'Dew Point °C'
    period = '19 Jan - 19 Feb 2020'

    records = sql_client.get_all_info_by_stations()
    index = DataHandler.get_index_of_value('Dew Point')
    lists_of_measurements = DataHandler.get_exact_value_from_many_my_sql_records(records, index)
    lists_of_measurements = DataHandler.get_lists_of_floats(lists_of_measurements)

    error_in_estimate = 1.0
    error_in_measurement = 1.0
    initial_estimate = 1.0
    lists_of_measurements = DataHandler.replace_none_with_dash(lists_of_measurements)

    lists_of_measurements = DataHandler.fill_missing_data_in_lists(lists_of_measurements)

    station_codes = DataHandler.get_station_codes()

    station_codes, lists_of_measurements = DataHandler.zip_codes_and_measurements(station_codes, lists_of_measurements)

    lists_of_estimates = KalmanFilter.get_lists_of_estimates(lists_of_measurements, error_in_estimate,
                                                             error_in_measurement)

    lists_of_estimates = DataHandler.get_lists_of_ints(lists_of_estimates)
    lists_of_measurements = DataHandler.get_lists_of_ints(lists_of_measurements)

    accuracies = DataHandler.get_accuracies(lists_of_measurements, lists_of_estimates)

    plt.barh(np.arange(len(accuracies)), accuracies)
    plt.yticks(np.arange(len(station_codes)), station_codes)
    plt.show()
