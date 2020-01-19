import requests
from bs4 import BeautifulSoup
from datetime import datetime

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


def get_current_fill_data() -> list:
    data_doc = []

    for data in get_data_list():
        data_dict = {'Station': data[0], 'Time': data[1], 'Date': get_date(), 'Dew Point': data[5]}
        data_doc.append(data_dict)

    return data_doc


def get_past_url(hour, day, month, year):
    return 'http://www.lvceli.lv/cms/index.php?h={}{:02d}{:02d}{:02d}'.format(year, month, day, hour)


def get_past_fill_data(hour: int, day: int, month: int, year: int) -> list:
    data_doc = []

    for data in get_data_list(get_past_url(hour, day, month, year)):
        data_dict = {'Station': data[0], 'Time': data[1], 'Date': get_date(), 'Dew Point': data[5]}
        data_doc.append(data_dict)

    return data_doc


def get_table(url):
    with requests.session() as s:
        r = s.post('http://www.lvceli.lv/cms/', data=login_data, headers=headers)

    soup = BeautifulSoup(r.content, 'html5lib')
    return soup.find("table", attrs={"class": "norm", "id": "table-1"})


def get_old_tables(url_modifiers: list) -> list:
    old_tables = []

    with requests.session() as s:
        r = s.post('http://www.lvceli.lv/cms/', data=login_data, headers=headers)

        for modifier in url_modifiers:
            r = s.get('http://www.lvceli.lv/cms/?h=' + modifier)
            soup = BeautifulSoup(r.content, 'html5lib')
            old_tables.append(soup.find("table", attrs={"class": "norm", "id": "table-1"}))

    return old_tables



