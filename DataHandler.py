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
    def get_list_of_station_names(list_of_lists_of_data: list) -> list:
        list_of_station_names = []

        for list_of_data in list_of_lists_of_data:
            list_of_station_names.append(list_of_data[-1])

        return list_of_station_names

    @staticmethod
    def get_list_of_lists_of_chosen_values(list_of_lists_of_dicts: list, value_name: str) -> list:
        list_of_values = []
        temp_list = []

        for list_of_dicts in list_of_lists_of_dicts:
            for data_dict in list_of_dicts:
                temp_list.append(data_dict[value_name])
            else:
                temp_list.append(data_dict['Station'])
            list_of_values.append(temp_list)
            temp_list = []

        return list_of_values

    @staticmethod
    def get_list_of_lists_of_measurements_with_station_names(lists_of_values: list) -> list:
        lists_of_measurements = []

        for list_of_values in lists_of_values:
            if '-' in list_of_values or '' in list_of_values:
                continue
            lists_of_measurements.append(DataHandler.get_list_of_float_numbers_and_station(list_of_values))

        return lists_of_measurements

    @staticmethod
    def get_list_of_lists_of_measurements_without_station_names(
            list_of_lists_of_measurements_with_station_names: list) -> list:
        list_of_lists_of_measurements_without_station_names = []

        for list_of_measurements in list_of_lists_of_measurements_with_station_names:
            list_of_measurements.pop(len(list_of_measurements) - 1)
            list_of_lists_of_measurements_without_station_names.append(list_of_measurements)

        return list_of_lists_of_measurements_without_station_names

    @staticmethod
    def get_prepared_lists_for_estimation(main_info) -> tuple:
        lists_of_values: list = DataHandler.get_list_of_lists_of_chosen_values(main_info, 'Dew Point')

        lists_of_measurements_with_station_names: list = DataHandler.get_list_of_lists_of_measurements_with_station_names(
            lists_of_values)

        list_of_station_names = DataHandler.get_list_of_station_names(lists_of_measurements_with_station_names)

        lists_of_measurements_without_station_names: list = DataHandler.get_list_of_lists_of_measurements_without_station_names(
            lists_of_measurements_with_station_names)

        lists_of_measurements: list = lists_of_measurements_without_station_names.copy()

        return lists_of_measurements, list_of_station_names
