from flask import render_template, Blueprint, current_app, request
from database.select import select_dict
from app.access import group_required
from  database.sql_provider import SQLProvider
import os

blueprint_query = Blueprint('query_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/query_menu', methods=['GET'])
@group_required
def query_menu():
    return render_template('query_menu.html')


@blueprint_query.route('/category', methods=['GET', 'POST'])
@group_required
def query_category():
    if request.method == 'POST':
        category = request.form['category']
        _sql = provider.get('client.sql', e_category=category)
        result = select_dict(current_app.config['db_config'], _sql)
        if result:
            prod_title = f'Все записи по категории {category}'
            print(result)
            return render_template('dynamic.html', prod_title=prod_title, products=result)
        else:
            return 'Результат не получен'
    else:
        return render_template('query_category.html')


@blueprint_query.route('/cost', methods=['GET', 'POST'])
@group_required
def query_cost():
    print(1)
    if request.method == 'POST':
        cost = request.form['cost']
        print(cost)
        _sql = provider.get('client.sql', e_cost=cost)
        result = select_dict(current_app.config['db_config'], _sql)
        print(result)
        if result:
            prod_title = f'Все записи по цене {cost} и меньше'
            print(result)
            return render_template('dynamic.html', prod_title=prod_title, products=result)
        else:
            return 'Результат не получен'
    else:
        return render_template('query_cost.html')