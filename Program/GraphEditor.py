from matplotlib import pyplot as plt
from matplotlib import pylab as plb


class GraphEditor:

    @staticmethod
    def create_plot(estimates: list, measurements: list, value: str, station_name: str):
        plt.plot(estimates, label='estimates')
        plt.plot(measurements, label='measurements')
        plt.title(station_name + ', ' + value)
        plt.legend()
        plt.show()
        # plot_name = station_name + '_' + value
        # plt.savefig(plot_name + '.png', bbox_inches='tight')

    @staticmethod
    def create_plots(lists_of_estimates: list, lists_of_measurements: list, station_names: list, value: str):
        for estimates, measurements, station_name in zip(lists_of_estimates, lists_of_measurements, station_names):
            GraphEditor.create_plot(estimates, measurements, value, station_name)

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
        for estimates, measurements, station_name in zip(lists_of_estimates, lists_of_measurements, station_names):
            plot = GraphEditor.create_plot(estimates, measurements, value, station_name)
            plot_name = station_name + '_' + value
            plot.savefig(plot_name, bbox_inches='tight')
