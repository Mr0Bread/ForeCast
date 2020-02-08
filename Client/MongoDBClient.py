import pymongo
from os.path import isfile


class MongoDBClient:
    def __init__(self, main_database_name: str, time_database_name: str):
        self.my_client = pymongo.MongoClient(
            "mongodb+srv://Mr0Bread:Elishka1Love@forecastcluster-ruxkg.gcp.mongodb.net/test?retryWrites=true&w=majority")
        self.main_database_name = main_database_name
        self.main_database = self.my_client[self.main_database_name]
        self.time_database_name = time_database_name
        self.time_database = self.my_client[self.time_database_name]
        self.is_it_first_filling = self.is_not_first_filling_made()

    def is_not_first_filling_made(self):
        file_name = 'first_filling.txt'

        if not isfile(file_name):
            print('creating {}'.format(file_name))

            with open(file_name, 'w') as file:
                if self.is_time_database_exists():
                    print(' Time_database exists and so returning False')
                    file.write('0')
                    return False
                else:
                    print(' Time database doesn\'t exist and so returning True')
                    file.write('1')
                    return True

        elif isfile(file_name):
            print('File exists')
            with open(file_name, 'r') as file:
                file_info = int(file.read())

                if file_info == 1 and not self.is_time_database_exists():
                    print(' return True')
                    return True
                else:
                    print(' return False')
                    return False

    def clear_collection(self, coll_name: str):
        self.main_database.drop_collection(coll_name)

    def clear_all_collections(self, coll_names: list):
        for name in coll_names:
            self.main_database.drop_collection(name)

    def get_collection(self, coll_name: str):
        return self.main_database[coll_name]

    def update_collection(self, coll_name: str, fill_data: dict):
        collection = self.get_collection(coll_name)
        collection.insert(fill_data)

    def delete_collection(self, coll_name: str):
        self.main_database[coll_name].drop()

    def get_collection_names(self) -> list:
        return self.main_database.list_collection_names()

    def fill_main_database(self, fill_data: list):
        for data_dict in fill_data:
            self.fill_collection(data_dict, data_dict['Station'])

    def fill_collection(self, data_dict: dict, coll_name: str):
        data_dict.pop('Station')

        collection = self.main_database[coll_name]
        collection.insert_one(data_dict)

    def get_relevant_fill_data_doc(self, fill_data: list) -> list:
        __fill_data = []
        for data_dict in fill_data:
            print(data_dict)
            if not self.is_imported_row_relevant(data_dict):
                print('removing row')
            else:
                print('adding row to returning list')
                __fill_data.append(data_dict)

        print(__fill_data)
        return __fill_data

    def update_time_database(self, fill_data: list):
        for data_dict in fill_data:
            collection = self.time_database[data_dict['Station']]
            collection.drop()
            collection.insert_one({'Time': data_dict['Time'], 'Date': data_dict['Date']})

    def is_imported_row_relevant(self, data_dict: dict) -> bool:
        collection = self.time_database[data_dict['Station']]
        search_result = collection.find({}, {'_id': 0, 'Time': 1, 'Date': 1})

        for selected_row in search_result:
            print('inside "for selected_row in search_result loop"')
            print(' Time in row ready to be imported: {}'.format(data_dict['Time']))
            print(' Time in selected row: {}'.format(selected_row['Time']))

            if data_dict['Time'] != selected_row['Time'] or data_dict['Date'] != selected_row['Date']:
                print('imported row is obsolete')
                return True
            else:
                print('imported row is still relevant')
                return False

    def fill_time_database(self, fill_data: list):
        print('Filling time database')
        if self.is_time_database_exists():
            print(' Deleting obsolete time database')
            self.delete_database(self.time_database_name)

        for data_dict in fill_data:
            collection = self.time_database[data_dict['Station']]
            collection.insert_one({'Time': data_dict['Time'], 'Date': data_dict['Date']})

    def is_time_database_exists(self) -> bool:
        database_list = self.my_client.list_database_names()
        if self.time_database_name in database_list:
            print('{} exists'.format(self.time_database_name))
            return True
        else:
            print('{} doesn\'t exists'.format(self.time_database_name))
            return False

    def delete_database(self, database_name: str):
        self.my_client.drop_database(database_name)

    def get_info_from_main_database(self) -> list:
        collection_names = self.main_database.list_collection_names()
        list_of_info = []
        temp_list = []
        for name in collection_names:
            for search_result in self.main_database[name].find():
                search_result.pop('_id')
                search_result['Station'] = name
                temp_list.append(search_result)
            list_of_info.append(temp_list)
            temp_list = []

        return list_of_info










