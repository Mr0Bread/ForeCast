from datetime import datetime


def get_year_start():
    error = True
    while error:
        error = False
        try:
            year_start = int(input('Enter start year\n'))
        except ValueError:
            print('Invalid input!')
            error = True
            continue

        if 2018 < year_start < datetime.now().year + 1:
            return year_start
        else:
            print('Invalid year value')
            error = True


def get_time_stamp_url_modifier() -> str:
    year_start = get_year_start()


get_year_start()
