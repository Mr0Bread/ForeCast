from Program.DataHandler import DataHandler
from Program.KalmanFilter import KalmanFilter
from Program.AutoDBFiller import AutoDBFiller
from Program.GraphEditor import GraphEditor
from Program.FileHandler import FileHandler
from Program.MySQLClient import MySQLClient
from Program.MongoDBClient import MongoDBClient
from Program.Request import Request

if __name__ == '__main__':
    sql_client = MySQLClient('139.59.212.33', 'outsider', 'password', 'forecast')

    value = 'Dew Point'

    records = sql_client.get_all_info_by_stations()
    index = DataHandler.get_index_of_value('Dew Point')
    lists_of_measurements = DataHandler.get_exact_value_from_many_my_sql_records(records, index)
    lists_of_measurements = DataHandler.get_lists_of_floats(lists_of_measurements)

    error_in_estimate = 1.0
    error_in_measurement = 1.0
    initial_estimate = 1.0
    i = 0
    for x in lists_of_measurements:
        i += 1
        print(x)
    else:
        print(i)
    #
    # graph = GraphEditor(list_of_estimates, init_list_of_measurements, value, 'LV01', 'Calculated')
    #
    # accuracies = DataHandler.get_estimation_accuracy([kf.get_list_of_estimates(), ], [list_of_measurements, ], ['LV01', ])
    #
    # FileHandler.write_a_set_of_data_to_file('estimation_log.txt', [list_of_measurements, ], [kf.get_list_of_estimates(), ],
    #                                         ['LV01', ], accuracies)
    #
    # graph.create_est_and_meas_plot()
    # graph.show_plot()
