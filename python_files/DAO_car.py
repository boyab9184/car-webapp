import json
import sqlite3

from years_data import years_data


class Dao:

    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        conn = sqlite3.connect("car.db")
        return conn

    @staticmethod
    def save_make(make_name, model, year, price, zip_code):
        conn = Dao.get_connection()

        sql = "INSERT INTO makes(make_name, model_name, year, price, zip) VALUES (?,?,?,?, ?)"
        conn.execute(sql, (make_name, model, year, price, zip_code))
        conn.commit()
        conn.close()

    @staticmethod
    def save_mrsp(mrsp):
        conn = Dao.get_connection()

        sql = "INSERT INTO makes(mrsp) VALUES (?)"
        conn.execute(sql, (mrsp))
        conn.commit()
        conn.close()

    @staticmethod
    def save_model(model_name):
        conn = Dao.get_connection()
        sql = "INSERT INTO models(model_name) VALUES (?)"
        conn.execute(sql, (model_name))
        conn.commit()
        conn.close()

    @staticmethod
    def save_makes_models(make_id, model_id):
        conn = Dao.get_connection()
        sql = 'INSERT INTO makes_models (make_id, model_id)) VALUES (?,?)'
        conn.execute(sql, (make_id, model_id))
        conn.commit()
        conn.close()

    @staticmethod
    def select():
        conn = Dao.get_connection()
        sql = 'SELECT * FROM movies'
        conn.execute(sql)
        conn.commit()
        conn.close()

    @staticmethod
    def graph_plot(make_list, model_list, year_range):
        years = years_data()
        price_car1 = 0
        price_car2 = 0
        years_car1 = []
        prices_car1 = []

        years_car2 = []
        prices_car2 = []

        conn = sqlite3.connect('car.db')
        c = conn.cursor()

        for year in year_range:
            c.execute('SELECT year, price FROM makes WHERE year=? AND make_name=? AND model_name=?;',
                      (year, make_list[0], model_list[0]))
            data_car1 = c.fetchall()
            c.execute('SELECT year, price FROM makes WHERE year=? AND make_name=? AND model_name=?;',
                      (year, make_list[1], model_list[1]))
            data_car2 = c.fetchall()

            for row in data_car1:
                price_car1 = price_car1 + row[1]
            try:
                prices_car1.append(int(price_car1 / len(data_car1)))
            except:
                prices_car1.append('NULL')
            years_car1.append(year)
            price_car1 = 0

            for row2 in data_car2:
                price_car2 = price_car2 + row2[1]
            try:
                prices_car2.append(int(price_car2 / len(data_car2)))
            except:
                prices_car2.append('NULL')
            years_car2.append(year)
            price_car2 = 0

        c.close()
        conn.close()

        graph_dict = {'x1': prices_car1, 'y1': years_car1,
                      'x2': prices_car2, 'y2': years_car2,
                      'makeModel1': make_list[0] + ', ' + model_list[0],
                      'makeModel2': make_list[1] + ', ' + model_list[1],
                      }

        # print (graph_dict)
        graph_data = json.dumps(graph_dict)

        return graph_dict

# if __name__ == "__main__":
#     Dao.graph_plot(['Honda', 'Toyota'], ['Accord', 'Camry'], [2010, 2011, 2012])
