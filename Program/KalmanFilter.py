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
        for measurement in self.__measurements:
            self.__measurement = measurement
            self.make_basic_calculations()

        else:
            return self.__estimate

    def get_list_of_estimates(self) -> list:
        list_of_estimates = []
        for measurement in self.__measurements:
            self.__measurement = measurement
            self.make_basic_calculations()
            list_of_estimates.append(self.__estimate)

        return list_of_estimates

    @staticmethod
    def get_initial_estimate_based_on_last_measurements(measurements: list) -> float:
        return measurements[-1] + (
                measurements[-1] - measurements[-2])

    @staticmethod
    def get_json_with_estimation():
        pass
