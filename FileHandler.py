from datetime import datetime


class FileHandler:

    @staticmethod
    def write_a_set_of_data_to_file(file_name: str, list_of_lists_of_measurements: list,
                                    list_of_lists_of_estimates: list,
                                    list_of_station_names: list, mode: str = 'a', encoding: str = 'utf-8'):
        with open(file_name, mode=mode, encoding=encoding) as file:
            file.write(str(datetime.now()) + '\n\n')
            for station_name, measurements, estimates in zip(list_of_station_names, list_of_lists_of_measurements,
                                                             list_of_lists_of_estimates):

                file.write(str(station_name) + '\n')

                for measurement in measurements:
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
