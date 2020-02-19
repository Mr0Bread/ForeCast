from matplotlib import pyplot as plt
from matplotlib import pylab as plb


class GraphEditor:
    def __init__(self, estimates: list, measurements: list, value: str, station_name: str, kalman_gain: float):
        self.estimates = estimates
        self.measurements = measurements
        self.value = value
        self.station_name = station_name
        self.kalman_gain = str(kalman_gain)
        self.plt = None

    def create_est_and_meas_plot(self):
        plt.plot(self.estimates, label='estimates', color='blue')
        plt.plot(self.measurements, label='measurements', color='orange')
        plt.title(self.station_name + ', ' + self.value + ' KG: ' + self.kalman_gain)
        plt.legend()
        self.plt = plt

    def create_est_plot(self):
        plt.plot(self.estimates, color='blue')
        plt.title('Estimates: ' + self.station_name + ', ' + self.value + ' KG: ' + self.kalman_gain)
        self.plt = plt

    def create_meas_plot(self):
        plt.plot(self.measurements, color='orange')
        plt.title('Measurements: ' + self.station_name + ', ' + self.value + ' KG: ' + self.kalman_gain)
        self.plt = plt

    def show_plot(self):
        self.plt.show()

    @staticmethod
    def create_plots(lists_of_estimates: list, lists_of_measurements: list, station_names: list, value: str):
        for estimates, measurements, station_name in zip(lists_of_estimates, lists_of_measurements, station_names):
            graph = GraphEditor(estimates, measurements, value, station_name, 0.9)
            # TODO

    @staticmethod
    def create_twolined_plot(lists_of_estimates: list, lists_of_measurements: list, value: str):
        __list_of_estimates = []
        __list_of_measurements = []

        for estimates, measurements in zip(lists_of_estimates, lists_of_measurements):
            for estimate in estimates:
                __list_of_estimates.append(estimate)

            for measurement in measurements:
                __list_of_measurements.append(measurement)
        else:
            plt.plot(__list_of_measurements, label='measurements', color='red')
            plt.plot(__list_of_estimates, label='estimates', color='green')
            plt.title('Twolined plot, ' + value)
            plt.legend()
            plt.show()

    @staticmethod
    def create_multilined_plot(lists_of_estimates: list, lists_of_measurements: list, value: str):
        for estimates, measurements in zip(lists_of_estimates, lists_of_measurements):
            plt.plot(estimates, color='green')
            plt.plot(measurements, color='red')
        else:
            plt.title('Multilined plot, ' + value)
            plt.show()

    @staticmethod
    def save_created_plots(lists_of_estimates: list, lists_of_measurements: list, station_names: list,
                           value: str):
        # TODO
        pass
