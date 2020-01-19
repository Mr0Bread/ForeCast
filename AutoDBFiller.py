from MongoDBExporter import MongoDBExporter
from datetime import datetime


def ask_start_day() -> int:
    pass


def get_time_period() -> dict:
    time_period = {}
    time_period['Start Day'] = ask_start_day()

    return time_period


class AutoDBFiller(MongoDBExporter):
    def __init__(self):
        super().__init__()

    def fill_collections_with_old_data(self):
        time_period = get_time_period()


get_time_period()
