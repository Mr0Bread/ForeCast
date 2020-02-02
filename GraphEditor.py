from matplotlib import pyplot as plt


class GraphEditor:

    @staticmethod
    def create_plot(estimates: list, measurements: list, title: str = ''):
        plt.plot(estimates, label='estimates')
        plt.plot(measurements, label='measurements')
        plt.title(title)
        plt.legend()
        plt.show()
