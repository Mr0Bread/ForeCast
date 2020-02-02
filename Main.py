from KalmanFilter import KalmanFilter
from FileHandler import FileHandler
from AutoDBFiller import AutoDBFiller
from DataHandler import DataHandler
from GraphEditor import GraphEditor

if __name__ == '__main__':
    filler = AutoDBFiller('MeteoInfoTable2', 'LastInsertTable2')
    main_info = filler.get_info_from_main_database()

    lists_of_measurements, station_names = DataHandler.get_prepared_lists_for_estimation(main_info)
    lists_of_estimates: list = []

    error_in_estimate = 0.3
    error_in_measurement = 0.1

    for measurements in lists_of_measurements:
        initial_estimate = KalmanFilter.get_initial_estimate_based_on_last_measurements(measurements)
        kf = KalmanFilter(error_in_estimate, initial_estimate, error_in_measurement, measurements)
        lists_of_estimates.append(kf.get_list_of_estimates())

    FileHandler.write_a_set_of_data_to_file('estimation_log.txt', lists_of_measurements,
                                            lists_of_estimates,
                                            station_names)

    GraphEditor.create_plots(lists_of_estimates, lists_of_measurements, station_names)
