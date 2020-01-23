import requests
from bs4 import BeautifulSoup
from threading import Thread
from time import sleep
from Request_data import headers, login_data, url
from MongoDBExporter import MongoDBExporter
from Request import get_fill_data_doc


class AutoDBFiller(MongoDBExporter):
    def __init__(self):
        super().__init__()
        self.thread = Thread()
        self.thread_is_running = False
        self.data = []

    def enable_realtime_data_collection(self, update_frequency_in_seconds: int = 180):
        self.thread = Thread(target=self.collect_data_in_realtime(update_frequency_in_seconds))
        self.thread_is_running = True
        self.thread.start()

    def collect_data_in_realtime(self, update_frequency_in_seconds):
        with requests.session() as s:
            while self.thread_is_running:
                sleep(update_frequency_in_seconds)
                print('collecting')
                request = s.post(url, login_data, headers=headers)
                soup = BeautifulSoup(request.content, 'html5lib')
                table = soup.find("table", attrs={"class": "norm", "id": "table-1"})
                fill_data = get_fill_data_doc(table)
                self.fill_database(fill_data)
                print('collecting finished')

    def disable_realtime_data_collection(self):
        self.thread_is_running = False


filler = AutoDBFiller()
filler.enable_realtime_data_collection()
