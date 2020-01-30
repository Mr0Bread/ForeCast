from threading import Thread
from time import sleep
from os import remove
from os.path import isfile

import requests
from bs4 import BeautifulSoup

from MongoDBClient import MongoDBClient
from Request import get_fill_data_doc
from Request_data import headers, login_data, url


def mark_first_filling(param: bool) -> bool:
    file_name = 'first_filling.txt'
    with open(file_name, 'w') as file:
        if not param:
            print('marked first filling with false')
            file.write('0')
            return False
        else:
            print('marked first filling with true')
            file.write('1')
            return True


class AutoDBFiller(MongoDBClient):
    def __init__(self,  main_database_name: str, time_database_name: str):
        super().__init__(main_database_name, time_database_name)
        self.thread = Thread()
        self.thread_is_running = False
        self.data = []

    def __del__(self):
        if isfile('first_filling.txt'):
            remove('first_filling.txt')

    def enable_realtime_data_collection(self, update_frequency_in_seconds: float = 10):
        self.thread_is_running = True
        self.thread = Thread(target=self.collect_data_in_realtime(update_frequency_in_seconds))
        print('starting thread')
        self.thread.start()

    def collect_data_in_realtime(self, update_frequency_in_seconds):
        print('creating session')
        with requests.session() as s:
            while self.thread_is_running:
                sleep(update_frequency_in_seconds)
                print(' collecting')
                request = s.post(url, login_data, headers=headers)
                soup = BeautifulSoup(request.content, 'html5lib')
                table = soup.find("table", attrs={"class": "norm", "id": "table-1"})
                fill_data_doc = get_fill_data_doc(table)

                if self.is_it_first_filling:
                    self.fill_time_database(fill_data_doc)
                    self.fill_main_database(fill_data_doc)
                    self.is_it_first_filling = mark_first_filling(False)
                    print('  First filling completed')
                else:
                    fill_data_doc = self.get_relevant_fill_data_doc(fill_data_doc)
                    self.update_time_database(fill_data_doc)
                    self.fill_main_database(fill_data_doc)
                    print('  Another filling completed')

                print(' collecting finished')

    def disable_realtime_data_collection(self):
        self.thread_is_running = False
        self.thread.join()
