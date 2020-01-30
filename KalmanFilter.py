from AutoDBFiller import AutoDBFiller
from datetime import datetime


class KalmanFilter:

    def __init__(self, initial_error_in_estimate, __initial_estimate, __error_in_measurement, __measurements,
                 number_of_tracked_values: int = 1):
        super().__init__()
        self.__number_of_tracked_values = number_of_tracked_values
        self.__measurements = __measurements
        self.__estimate = __initial_estimate
        self.__error_in_estimate = initial_error_in_estimate
        self.__error_in_measurement = __error_in_measurement
        self.__measurement = None
        self.__kalman_gain = None

    def set_measurements(self, __measurements):
        self.__measurements = __measurements

    def get_measurements(self):
        return self.__measurements

    def update_values(self, __measurements):
        self.set_measurements(__measurements)

    def __calculate_kalman_gain(self) -> float:
        return self.__error_in_estimate / (self.__error_in_estimate + self.__error_in_measurement)

    def __calculate_estimate(self) -> float:
        return self.__estimate + self.__kalman_gain * (self.__measurement - self.__estimate)

    def __calculate_error_in_estimate(self) -> float:
        return (1 - self.__kalman_gain) * self.__error_in_estimate

    def make_basic_calculations(self):
        self.__kalman_gain = self.__calculate_kalman_gain()
        self.__estimate = self.__calculate_estimate()
        self.__error_in_estimate = self.__calculate_error_in_estimate()

    def get_current_estimate(self):
        for __measurement in self.__measurements:
            self.__measurement = __measurement
            self.make_basic_calculations()

        else:
            return self.__estimate

    def get_list_of_estimates(self) -> list:
        __list_of_estimates = []
        for __measurement in self.__measurements:
            self.__measurement = __measurement
            self.make_basic_calculations()
            __list_of_estimates.append(self.__estimate)

        return __list_of_estimates


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


def write_data_to_file(file_name: str, __list_of_lists_of_measurements: list,
                       __list_of_lists_of_estimates: list,
                       __list_of_station_names: list, mode: str = 'a', encoding: str = 'utf-8'):
    with open(file_name, mode=mode, encoding=encoding) as file:
        file.write(str(datetime.now()) + '\n\n')

        for station_name, __measurements, estimates in zip(__list_of_station_names, __list_of_lists_of_measurements,
                                                           __list_of_lists_of_estimates):
            file.write(str(station_name) + '\n')

            for measurement in __measurements:
                file.write(str(measurement) + ' , ')
            else:
                file.write('\n')

            for estimate in estimates:
                file.write(str(estimate) + ' , ')
            else:
                file.write('\n\n')

            file.write('Last estimate: {}\n'.format(estimates[-2]))
            file.write('True value: {}\n\n'.format(measurements[-1]))
        else:
            file.write('\n\n\n')


write_data_to_file('estimation_log.txt', list_of_lists_of_measurements, list_of_lists_of_estimates,
                   list_of_station_names)
