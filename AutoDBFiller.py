from MongoDBExporter import MongoDBExporter
from datetime import datetime


def get_url_modifier() -> str:
    pass


class AutoDBFiller(MongoDBExporter):
    def __init__(self):
        super().__init__()

    def fill_collections_with_old_data(self):
        url_modifier = get_url_modifier()
