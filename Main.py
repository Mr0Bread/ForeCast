from KalmanFilter import KalmanFilter
from FileHandler import FileHandler
from AutoDBFiller import AutoDBFiller


if __name__ == '__main__':
    filler = AutoDBFiller('MeteoInfoTable', 'LastInsertTable')
    main_info = filler.get_list_of_info_from_main_database()
    list_of_lists_of_values = filler.get_list_of_values(main_info, 'Dew Point')
    list_of_lists_of_measurements = filler.get_list_of_lists_of_measurements(list_of_lists_of_values)
    list_of_station_names = filler.get_list_of_station_names(main_info)
    list_of_lists_of_estimates = []

    error_in_estimate = 0.3
    error_in_measurement = 0.1

    for measurements in list_of_lists_of_measurements:
        initial_estimate = measurements[-1] + (
                measurements[-1] - measurements[-2])
        kf = KalmanFilter(error_in_estimate, initial_estimate, error_in_measurement, measurements)
        list_of_lists_of_estimates.append(kf.get_list_of_estimates())

    FileHandler.write_a_set_of_data_to_file('estimation_log.txt', list_of_lists_of_measurements,
                                            list_of_lists_of_estimates,
                                            list_of_station_names)
