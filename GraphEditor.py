from matplotlib import pyplot as plt


class GraphEditor:

    @staticmethod
    def create_plot(estimates: list, measurements: list, title: str = ''):
        plt.plot(estimates, label='estimates')
        plt.plot(measurements, label='measurements')
        plt.title(title)
        plt.legend()
        plt.show()

    @staticmethod
    def create_plots(lists_of_estimates: list, lists_of_measurements: list, station_names: list):
        for estimates, measurements, station_name in zip(lists_of_estimates, lists_of_measurements, station_names):
            GraphEditor.create_plot(estimates, measurements, station_name)
