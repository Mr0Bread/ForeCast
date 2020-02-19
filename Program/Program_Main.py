from Program.DataHandler import DataHandler
from Program.KalmanFilter import KalmanFilter
from Program.AutoDBFiller import AutoDBFiller
from Program.GraphEditor import GraphEditor
from Program.FileHandler import FileHandler
from Program.MySQLClient import MySQLClient

if __name__ == '__main__':
    sql_client = MySQLClient('139.59.212.33', 'outsider', 'password', 'forecast')
    value = 'Dew Point'

    records = sql_client.get_info_by_station()

    index = DataHandler.get_index_of_value(value)
    list_of_measurements = DataHandler.get_exact_value_from_my_sql_records(records, index)
    list_of_measurements = DataHandler.get_list_of_floats(list_of_measurements)

    error_in_estimate = 1.0
    error_in_measurement = 1.0

    kf = KalmanFilter(error_in_estimate, 3.0, error_in_measurement, list_of_measurements)

    graph = GraphEditor(kf.get_list_of_estimates(), list_of_measurements, value, 'LV01', 0.9)

    accuracies = DataHandler.get_estimation_accuracy([kf.get_list_of_estimates(), ], [list_of_measurements, ], ['LV01', ])

    FileHandler.write_a_set_of_data_to_file('estimation_log.txt', [list_of_measurements, ], [kf.get_list_of_estimates(), ],
                                            ['LV01', ], accuracies)
