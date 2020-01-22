import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from TimeStamps import TimeStamps
import threading

login_data = {
    "login": "demo",
    "password": "demo"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.108 Safari/537.36 '
}


def get_data_list(url="http://www.lvceli.lv/cms/") -> list:
    tmp_list = []
    data_list = []
    table = get_table(url)

    for row in table.find_all('tr'):
        for cell in row.find_all('td'):
            tmp_list.append(cell.text)

        while len(tmp_list) < 19:
            tmp_list.append('-')

        data_list.append(tmp_list)
        tmp_list = []

    data_list.pop(0)
    return data_list


def get_date() -> str:
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year

    return 'Year: {} Month: {} Day: {}'.format(year, month, day)


def get_current_fill_data_doc() -> list:
    data_doc = []

    for data in get_data_list():
        data_dict = {'Station': data[0], 'Time': data[1], 'Date': get_date(), 'Dew Point': data[5]}
        data_doc.append(data_dict)

    return data_doc


def get_table(url):
    with requests.session() as s:
        r = s.post('http://www.lvceli.lv/cms/', data=login_data, headers=headers)

    soup = BeautifulSoup(r.content, 'html5lib')
    return soup.find("table", attrs={"class": "norm", "id": "table-1"})


def get_old_tables(modified_urls: list) -> list:
    old_tables = []

    with requests.session() as s:
        r = s.post('http://www.lvceli.lv/cms/', data=login_data, headers=headers)

        for url in modified_urls:
            r = s.get(url)
            soup = BeautifulSoup(r.content, 'html5lib')
            old_tables.append(soup.find("table", attrs={"class": "norm", "id": "table-1"}))

    return old_tables


def get_time_stamps() -> dict:
    time_stamps = TimeStamps()
    return time_stamps.get()


def get_valid_dates(time_stamps) -> list:
    valid_dates = []

    year_start = time_stamps['Year Start']
    year_stop = time_stamps['Year Stop']

    month_start = time_stamps['Month Start']
    month_stop = time_stamps['Month Stop']

    day_start = time_stamps['Day Start']
    day_step = time_stamps['Day Step']
    day_stop = time_stamps['Day Stop']

    hour_start = time_stamps['Hour Start']
    hour_step = time_stamps['Hour Step']
    hour_stop = time_stamps['Hour Stop']

    date_start = datetime(year_start, month_start, day_start, hour_start, 0, 0)
    date_stop = datetime(year_stop, month_stop, day_stop, hour_stop, 0, 0)
    date_step = timedelta(days=day_step, hours=hour_step)
    date_next = date_start + date_step

    while date_next <= date_stop:
        valid_dates.append(date_next)
        date_next += date_step

    return valid_dates


def transform_date_into_url_modifier(date) -> str:
    return '{}{:02d}{:02d}{:02d}'.format(date.year, date.month, date.day, date.hour)


def get_url_modifiers() -> list:
    url_modifiers = []

    valid_dates = get_valid_dates(get_time_stamps())

    for date in valid_dates:
        url_modifiers.append(transform_date_into_url_modifier(date))

    return url_modifiers


def get_modified_urls():
    modified_urls = []
    for modifier in get_url_modifiers():
        modified_urls.append('http://www.lvceli.lv/cms/index.php?h=' + modifier)

    return modified_urls


def get_data_from_old_tables(old_tables) -> list:
    data = []
    rows = []
    cells = []
    for table in old_tables:
        for row in table.find_all('tr'):
            for cell in row.find_all('td'):
                cells.append(cell.text)
            rows.append(cells)
            cells = []
        rows.pop(0)
        data.append(rows)
        rows = []

    return data


def get_data_doc_from_data(data: list) -> list:
    data_doc = []
    for table in data:
        for row in table:
            if len(row) < 19:
                continue
            else:
                data_doc.append({'Station': row[0], 'Time': row[1], 'Dew Point': row[5]})

    return data_doc


def enable_realtime_data_collecting(update_frequency_in_seconds: int, samples_quantity: int):
    pass
