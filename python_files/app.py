import json

from flask import Flask, jsonify

from DAO_car import Dao
from python_files.controller_car import handle_car_api_data, handle_data
from python_files.program_manager import budget_search_manager, new_car_years
from queryMarketCheck import Query

app = Flask(__name__, template_folder='ui\src\index.html')


@app.route('/search_make/<make>', methods=['GET'])
def search_make(make):
    model = []
    if make == 'Honda':
        model = ["Civic", "Accord"]
        print(model)
    elif make == 'BMW':
        model = ['3 Series', '5 Series', 'X3', 'X5']
        print(model)
    elif make == 'Audi':
        model = ['A4', 'A6', 'Q5', 'Q7']
        print(model)

    elif make == 'Toyota':
        model = ['Corolla', 'Camry', 'RAV4']

    elif make == 'Nissan':
        model = ['Sentra', 'Altima']

    model_jason = json.dumps(model)

    return model_jason


@app.route('/search-car/<zip_code>/<year>/<make>/<model>/', methods=['GET'])
def search_car(zip_code, year, make, model, state):
    """Call on queryMarket to search for the car on Market Check API"""
    make_list = make.split(',')
    model_list = model.split(',')

    ymm = year + '%7C' + str(make_list[0]) + '%7C' + str(model_list[0]) + '%2C' + year + '%7C' + str(make_list[1]) \
          + '%7C' + str(model_list[1])

    car_dict = Query.search1(zip_code, ymm, state)
    graph_data = handle_car_api_data(car_dict)

    return graph_data


@app.route('/search-cars/<zip_code>/<from_year>/<to_year>/<make>/<model>', methods=['GET'])
def search_car1(zip_code, from_year, to_year, make, model):
    make_list = make.split(',')
    model_list = model.split(',')
    zip_code_list = zip_code.split(',')

    from_year_list = from_year.split(',')
    to_year_list = to_year.split(',')

    from_year_list = [int(x) for x in from_year_list]
    from_year_list.sort()
    to_year_list = [int(x) for x in to_year_list]
    to_year_list.sort(reverse=True)

    if from_year_list[0] == to_year_list[0]:
        year_range = from_year_list[0]

    else:
        year_range = list(range(from_year_list[0], to_year_list[0] + 1))

    photo_list = []
    aux_list = []
    for i in range(len(make_list)):
        for j in year_range:
            year = str(j)
            car_dict = Query().search2(zip_code_list[i], year, make_list[i], model_list[i])
            handle_data(car_dict, zip_code_list[i])
            # time.sleep(1)

            if car_dict['listings'][i]['build']['model'] not in aux_list:
                while len(photo_list) < 2:
                    photo_list.append(car_dict['listings'][i]['media']['photo_links'][1])
                    aux_list.append(car_dict['listings'][i]['build']['model'])
                    break

    graph_dict = Dao.graph_plot(make_list, model_list, year_range)
    graph_dict['photo1'] = photo_list[0]
    graph_dict['photo2'] = photo_list[1]

    graph_data = json.dumps(graph_dict)

    return graph_data


@app.route('/search-budget/<budget>/<car_type>/<milieage>/<zip_code>/<color>', methods=['GET'])
def budget_search(budget, car_type, milieage, zip_code, color):
    budget_dict = budget_search_manager(budget, car_type, milieage, zip_code, color)
    budget_data = jsonify(budget_dict)

    return budget_data


@app.route('/search-newcar/<make>/<model>/<zip_code>', methods=['GET'])
def new_car_search(make, model, zip_code):
    new_car_graph_data = new_car_years(make, model, zip_code)

    return new_car_graph_data


if __name__ == "__main__":
    app.run(debug=True)
