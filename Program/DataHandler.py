class DataHandler:

    @staticmethod
    def get_list_of_float_numbers_and_station(list_of_values: list) -> list:
        list_of_data = []

        for value in list_of_values:
            try:
                list_of_data.append(float(value))
            except ValueError:
                list_of_data.append(value)

        return list_of_data

    @staticmethod
    def get_corresponding_list_of_time(data_list: list) -> list:
        list_of_time = []
        temp_list = []
        for list_of_dicts in data_list:
            for data_dict in list_of_dicts:
                temp_list.append(data_dict['Time'])
            else:
                temp_list.append(data_dict['Station'])
            list_of_time.append(temp_list)
            temp_list = []
        return list_of_time

    @staticmethod
    def zip_time_and_values(lists_of_values: list, lists_of_time: list) -> list:
        zipped_list = []
        temp_list1 = []
        temp_list2 = []
        temp_list3 = []
        station_names = []

        for list_of_values in lists_of_values:
            station_names.append(list_of_values[len(list_of_values) - 1])
            list_of_values.pop(len(list_of_values) - 1)
            temp_list1.append(list_of_values)
        else:
            for list_of_time in lists_of_time:
                list_of_time.pop(len(list_of_time) - 1)
                temp_list2.append(list_of_time)

            for value, time, station_name in zip(temp_list1, temp_list2, station_names):
                temp_list3.append(station_name)
                temp_list3.append(value)
                temp_list3.append(time)
                zipped_list.append(temp_list3)
                temp_list3 = []

        return zipped_list

    @staticmethod
    def get_station_names(list_of_lists_of_data: list) -> list:
        list_of_station_names = []

        for list_of_data in list_of_lists_of_data:
            list_of_station_names.append(list_of_data[-1])

        return list_of_station_names

    @staticmethod
    def get_lists_of_chosen_values(lists_of_dicts: list, value_name: str) -> list:
        list_of_values = []
        temp_list = []

        for list_of_dicts in lists_of_dicts:
            for data_dict in list_of_dicts:
                temp_list.append(data_dict[value_name])
            else:
                temp_list.append(data_dict['Station'])
            list_of_values.append(temp_list)
            temp_list = []

        return list_of_values

    @staticmethod
    def get_lists_of_measurements_with_station_names(lists_of_values: list) -> list:
        lists_of_measurements = []

        for list_of_values in lists_of_values:
            if '-' in list_of_values or '' in list_of_values:
                continue
            lists_of_measurements.append(DataHandler.get_list_of_float_numbers_and_station(list_of_values))

        return lists_of_measurements

    @staticmethod
    def get_lists_of_measurements_without_station_names(
            list_of_lists_of_measurements_with_station_names: list) -> list:
        list_of_lists_of_measurements_without_station_names = []

        for list_of_measurements in list_of_lists_of_measurements_with_station_names:
            list_of_measurements.pop(len(list_of_measurements) - 1)
            list_of_lists_of_measurements_without_station_names.append(list_of_measurements)

        return list_of_lists_of_measurements_without_station_names

    @staticmethod
    def get_prepared_lists_for_estimation(main_info, value: str = 'Dew Point') -> tuple:
        lists_of_values: list = DataHandler.get_lists_of_chosen_values(main_info, value)

        lists_of_measurements_with_station_names: list = DataHandler.get_lists_of_measurements_with_station_names(
            lists_of_values)

        list_of_station_names = DataHandler.get_station_names(lists_of_measurements_with_station_names)

        lists_of_measurements_without_station_names: list = DataHandler.get_lists_of_measurements_without_station_names(
            lists_of_measurements_with_station_names)

        lists_of_measurements: list = lists_of_measurements_without_station_names.copy()

        return lists_of_measurements, list_of_station_names

    @staticmethod
    def get_estimation_accuracy(lists_of_estimates: list, lists_of_measurements: list, station_names: list):
        from math import sqrt

        dict_of_accuracy = {}

        number_of_estimations = len(lists_of_measurements)

        for estimates, measurements, station_name in zip(lists_of_estimates, lists_of_measurements, station_names):
            sum_of_differences = 0

            for estimate, measurement in zip(estimates, measurements):
                sum_of_differences += estimate - measurement
            else:
                dict_of_accuracy[station_name] = sqrt((sum_of_differences ** 2) / number_of_estimations)

        return dict_of_accuracy

    @staticmethod
    def get_json(lists_of_values):
        json_dict = {}
        temp_list = []

        for list_of_values in lists_of_values:
            for value in list_of_values[0:-2]:
                temp_list.append(value)
            else:
                json_dict[list_of_values[-1]] = temp_list
                temp_list = []

        return json_dict

    @staticmethod
    def get_json_of_existing_values():
        return {'Values': ['Station',
                           'Time',
                           'Air Temperature',
                           'Air Temperature(-1 h)',
                           'Humidity',
                           'Dew Point',
                           'Precipitation',
                           'Intensity',
                           'Visibility',
                           'Road Temperature',
                           'Road Temperature(-1 h)',
                           'Road Condition',
                           'Road Warning',
                           'Freezing Point',
                           'Road Temperature 2',
                           'Road Temperature 2(-1 h)',
                           'Road Condition 2',
                           'Road Warning 2',
                           'Freezing Point 2']}

    @staticmethod
    def get_json_of_station_names():
        return {'Stations': ['A1 km 12 Ādaži',
                             'A1 km 21 Lilaste',
                             'A1 km 39 Skulte',
                             'A1 km 45 Dunte',
                             'A1 km 57 Tūja',
                             'A1 km 71 Vitrupe',
                             'A1 km 9 Ādaži',
                             'A1 km 97 Ainaži',
                             'A2 km 102 Rauna',
                             'A2 km 126 Smiltene',
                             'A2 km 156 Vireši',
                             'A2 km 27 Garkalne',
                             'A2 km 57 Sigulda',
                             'A2 km 76 Melturi',
                             'A3 km 102 Strenči',
                             'A3 km 24 Inciems',
                             'A3 km 41 Stalbe',
                             'A3 km 62 Valmiera',
                             'A4 km 7 Mucenieki',
                             'A5 km 23 Apvedceļš',
                             'A5 km 8 Ķekava',
                             'A6 km 109 Ādmiņi',
                             'A6 km 163 Līvāni',
                             'A6 km 200 Nīcgale',
                             'A6 km 22 Saulkalne',
                             'A6 km 236 Daugavpils',
                             'A6 km 280 Krāslava',
                             'A6 km 63 Kaibala',
                             'A7 km 32 Bērziņi',
                             'A7 km 53 Zariņi',
                             'A7 km 71 Ceraukste',
                             'A7 km 82 Grenctāle',
                             'A8 km 27 Dalbe',
                             'A8 km 43 Vircava',
                             'A8 km 72 Eleja',
                             'A9 km 113 Saldus',
                             'A9 km 13 Lāči',
                             'A9 km 138 Rudbārži',
                             'A9 km 154 Kalvene',
                             'A9 km 178 Durbe',
                             'A9 km 24 Kalnciems',
                             'A9 km 39 Apšupe',
                             'A9 km 62 Annenieki',
                             'A10 km 104 Talsi',
                             'A10 km 138 Usma',
                             'A10 km 169 Pope',
                             'A10 km 17 Jūrmala',
                             'A10 km 36 Sloka',
                             'A10 km 45 Ķemeri',
                             'A10 km 80 Pūre',
                             'A11 km 38 Nīca',
                             'A12 km 155 Zilupe',
                             'A12 km 38 Atašiene',
                             'A12 km 68 Viļāni',
                             'A12 km 96 Rēzekne',
                             'A13 km 11 Kārsava',
                             'A13 km 81 Feimaņi',
                             'P80 km 13 Ogresgals',
                             'P80 km 35 Zādzene']}

    @staticmethod
    def is_possible_to_fill_missing_data(list_of_values: list) -> bool:
        index = 0
        adder = 1

        while adder < 5 and index < len(list_of_values) - 1 and index + adder < len(list_of_values):
            if list_of_values[index] == '-' and list_of_values[index + adder] == '-':
                adder += 1
            else:
                index += adder
                adder = 1
        else:
            if adder > 4:
                return False
            else:
                return True

    @staticmethod
    def get_indexes_for_filling(list_of_values: list) -> tuple:

        index = 0
        adder = 1

        indexes = []

        while adder < 5 and index < len(list_of_values) - 1 and index + adder < len(list_of_values):
            if adder == 1 and list_of_values[index] == '-' and list_of_values[index + 1] != '-':
                indexes.append([index, 'one'])

            if list_of_values[index] == '-' and list_of_values[index + adder] == '-':
                adder += 1
            elif adder != 1:
                indexes.append([index - 1, index + adder, adder, 'normal'])
                index += adder
                adder = 1
            else:
                index += adder
                adder = 1
        else:
            if adder != 1:
                indexes.append([index - 1, index + adder - 1, adder, 'in the end'])

        return tuple(indexes)

