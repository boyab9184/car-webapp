import sqlite3

from numpy import median

from DAO_car import Dao


def handle_car_api_data(car_dict):

    car_price = []
    for i in range(len(car_dict['listings'])):
        try:
            list_price = car_dict['listings'][i]['price']
            car_price.append(list_price)
        except:
            continue

    price = round(median(car_price), 0)
    make = []
    model = []
    year = car_dict['listings'][0]['build']['year']
    zip_code = car_dict['listings'][0]['dealer']['zip']

    for i in range(len(car_dict['listings'])):
        try:
            make_elem = car_dict['listings'][i]['build']['make']
            model_elem = car_dict['listings'][i]['build']['model']
            if make_elem not in make:
                make.append(make_elem)
            elif model_elem not in model:
                model.append(model_elem)

        except:
            continue

    Dao.save_make(make[0], model[0], year, price, zip_code)
    Dao.save_make(make[1], model[1], year, price, zip_code)
    graph_data = Dao.graph_plot(make, model, 2011)

    return graph_data


def handle_data(car_dict, zip_code):
    make = ''
    model = ''
    year = None

    for i in range(len(car_dict['listings'])):
        while make != '' and model != '' and year is not None:
            make = car_dict['listings'][i]['build']['make']
            model = car_dict['listings'][i]['build']['model']
            year = car_dict['listings'][i]['build']['year']
            break

    if 'median' in car_dict['stats']['price']:
        price = car_dict['stats']['price']['median']
    else:
        car_price = []
        for i in range(len(car_dict['listings'])):
            try:
                list_price = car_dict['listings'][i]['price']
                car_price.append(list_price)

            except:
                continue

        price = round(median(car_price), 0)

    Dao.save_make(make, model, year, price, zip_code)


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        conn = sqlite3.connect("car.db")
        return conn
