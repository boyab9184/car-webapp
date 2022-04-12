from datetime import datetime


def years_data():
    current_year = datetime.now().year
    years_list = []
    for year in range(current_year, current_year - 10, -1):
        years_list.append(year)

    years_list.append(current_year - 10)

    return years_list
