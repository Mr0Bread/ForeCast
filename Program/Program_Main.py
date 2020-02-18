from Program.DataHandler import DataHandler
from Program.KalmanFilter import KalmanFilter
from Program.AutoDBFiller import AutoDBFiller
from Program.GraphEditor import GraphEditor
from Program.FileHandler import FileHandler
from Program.MySQLClient import MySQLClient

if __name__ == '__main__':
    sql_client = MySQLClient('139.59.212.33', 'outsider', 'password', 'forecast')
    value = 'Air Temperature'

    records = sql_client.get_info_by_station()

    index = DataHandler.get_index_of_value(value)
    values = DataHandler.get_exact_value_from_my_sql_records(records, index)
    values = DataHandler.get_list_of_floats(values)

    graph_editor = GraphEditor()
    filler = AutoDBFiller('MeteoInfoTable2', 'LastInsertTable2')
    main_info = filler.get_info_from_main_database()

    # lists_of_measurements, station_names = DataHandler.get_prepared_lists_for_estimation(main_info, value)
    lists_of_estimates = []

    error_in_estimate = 1.0
    error_in_measurement = 1.0

    graph_editor.create_plot(lists_of_estimates[0], values, value, 'LV01')

    # accuracies = DataHandler.get_estimation_accuracy(lists_of_estimates, lists_of_measurements, station_names)

    # FileHandler.write_a_set_of_data_to_file('estimation_log.txt', lists_of_measurements, lists_of_estimates, station_names, accuracies)
