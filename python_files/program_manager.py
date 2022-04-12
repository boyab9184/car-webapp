import json
import operator
from datetime import datetime

from numpy import median

from queryMarketCheck import Query


def budget_search_manager(budget, car_type, mileage, zip_code, color):
    budget_range_tup = (int(budget) - 500, int(budget) + 500)
    budget_range_str = str(budget_range_tup[0]) + '-' + str(budget_range_tup[1])
    mileage_range_str = '0-' + mileage
    if mileage != 'any':
        budget_dict = Query.budget_search(budget_range_str, car_type, mileage_range_str, zip_code, color)
    else:
        budget_dict = Query.budget_search_anymileage(budget_range_str, car_type, zip_code, color)

    sorted_dict = sort_mileage(budget_dict)

    return sorted_dict


def sort_mileage(budget_dict):
    list_of_dicts = budget_dict['listings']
    list_of_dicts.sort(key=operator.itemgetter('miles'))

    luxury_list = ['BMW', "Lexus", 'Audi', 'Mercedes', 'Infiniti', 'Acura', 'Cadillac', 'Lincoln', 'Porsche',
                   'Land Rover', 'Volvo']
    domestic_list = ['Chevrolet', 'Dodge', 'Ram', 'Ford', 'Chrysler']
    foreign_list = ['Honda', 'Toyota', 'Mazda']
    rec_list = []
    aux_list = []

    for make in luxury_list:
        if len(aux_list) < 2:
            for i in range(len(list_of_dicts)):
                if make == list_of_dicts[i]['build']['make'] and make not in aux_list:
                    rec_list.append(list_of_dicts[i])
                    aux_list.append(make)
        else:
            break

    if len(rec_list) < 2:
        rec_list = []
        aux_list = []
        while len(rec_list) < 2:
            for make in luxury_list:
                if len(aux_list) < 2:
                    for i in range(len(list_of_dicts)):
                        if make == list_of_dicts[i]['build']['make']:
                            rec_list.append(list_of_dicts[i])
                            aux_list.append(make)
                else:
                    break

    aux_list = []
    for make1 in domestic_list:
        for j in range(len(list_of_dicts)):
            if len(aux_list) < 2:
                if make1 == list_of_dicts[j]['build']['make'] and make1 not in aux_list:
                    rec_list.append(list_of_dicts[j])
                    aux_list.append(make1)
            else:
                break

    aux_list = []
    for make2 in foreign_list:
        for k in range(len(list_of_dicts)):
            if len(aux_list) < 2:
                car = list_of_dicts[k]['build']['make']
                if make2 == car and make2 not in aux_list:
                    rec_list.append(list_of_dicts[k])
                    aux_list.append(make2)
            else:
                break

    return rec_list


class Manage_budget_data:
    def __init__(self):
        pass


def new_car_years(make, model, zip_code):
    median_price_list = []
    new_car_dict = Query.new_car_search(make, model, zip_code)
    median_price_list.append(Manage_new_car_search().roundup(int(new_car_dict['stats']['price']['median'])))
    years_list = Manage_new_car_search().years_data()
    for year in years_list:
        new_car_years_dict = Query.new_car_search_years(make, model, zip_code, year)

        try:
            median_price = int(new_car_years_dict['stats']['price']['median'])
            median_price_roundup = Manage_new_car_search().roundup(median_price)
        except:
            median_price_roundup = None

        median_price_list.append(median_price_roundup)

    current_year = datetime.now().year
    years_list.insert(0, str(current_year))
    years_list[-1] = str(current_year - 20)
    years_list.append(str(current_year - 30))

    ninetees_data = ninetees_data(make, model)

    median_price_list.append(ninetees_data[0])
    photo_nineties = ninetees_data[1]

    photo = ''
    for i in range(len(new_car_dict['listings'])):
        try:
            photo = new_car_dict['listings'][i]['media']['photo_links'][0]
            pass
        except:
            continue

    graph_dict = {'y1': median_price_list,
                  'x1': years_list,
                  'make_model': make + ', ' + model,
                  'photo': photo,
                  'photo_nine': photo_nineties}

    new_car_graph_data = json.dumps(graph_dict)

    return new_car_graph_data


def ninetees_data(make, model):
    current_year = datetime.now().year

    years_str = str(current_year - 29) + ',' + str(current_year - 28) + ',' + str(current_year - 27)
    nineties_car_dict = Query.nintees_car_search(years_str, make, model)
    car_price = []
    photo_nineties = ''
    for i in range(len(nineties_car_dict['listings'])):
        try:
            list_price = nineties_car_dict['listings'][i]['price']
            car_price.append(list_price)
        except:
            continue

    try:
        price = int(median(car_price))
        price_roundup = Manage_new_car_search().roundup(price)
    except:
        price_roundup = None

    for i in range(len(nineties_car_dict['listings'])):
        try:
            photo_nineties = nineties_car_dict['listings'][i]['media']['photo_links'][1]
            pass
        except:
            photo_nineties = ''

    return price_roundup, photo_nineties


class Manage_new_car_search:
    def __init__(self):
        pass

    @staticmethod
    def years_data():
        curent_year = datetime.now().year
        years_list = []

        for year in range(curent_year - 1, curent_year - 8, -2):
            years_list.append(year)
        years_list.append(curent_year - 10)
        years_list_str = [str(year) for year in years_list]
        twenty_years_str = str(curent_year - 18) + ',' + str(curent_year - 19) + ',' + str(curent_year - 20)
        years_list_str.append(twenty_years_str)

        return years_list_str

    @staticmethod
    def roundup(x):
        return x if x % 100 == 0 else x + 100 - x % 100
