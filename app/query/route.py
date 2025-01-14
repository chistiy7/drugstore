from flask import render_template, Blueprint, current_app, request
from database.select import select_dict
from app.access import group_required
from database.sql_provider import SQLProvider
import os

blueprint_query = Blueprint('query_bp', __name__, template_folder='templates')


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/query_menu', methods=['GET'])
@group_required
def query_menu():
    return render_template('query_menu.html')


@blueprint_query.route('/medicine', methods=['GET', 'POST'])
@group_required
def query_medicine():
    if request.method == 'POST':
        medicine = request.form['medicine']
        print(medicine)
        _sql = provider.get('medicine.sql', input_medicine=medicine)
        result = select_dict(current_app.config['db_config'], _sql)
        if result:
            prod_title = f'Все записи по препарату с названием {medicine}'
            print(result)
            return render_template('dynamic.html', prod_title=prod_title, products=result)
        else:
            return 'Результат не получен'
    else:
        return render_template('query_medicine.html')


@blueprint_query.route('/group', methods=['GET', 'POST'])
@group_required
def query_group():
    if request.method == 'POST':
        group = request.form['group']
        print(group)
        _sql = provider.get('medicine_group.sql', input_group=group)
        result = select_dict(current_app.config['db_config'], _sql)
        print(result)
        if result:
            prod_title = f'Все записи по препарату группы {group}'
            print(result)
            return render_template('dynamic.html', prod_title=prod_title, products=result)
        else:
            return 'Результат не получен'
    else:
        return render_template('query_group.html')

# @blueprint_query.route('/orders', methods=['GET', 'POST'])
# @group_required
# def query_group():
#     if request.method == 'POST':
#         order = request.form['order']
#         print(order)
#         _sql = provider.get('medicine_group.sql', input_order=order)
#         result = select_dict(current_app.config['db_config'], _sql)
#         print(result)
#         if result:
#             prod_title = f'Все  по препарату группы {group}'
#             print(result)
#             return render_template('dynamic.html', prod_title=prod_title, products=result)
#         else:
#             return 'Результат не получен'
#     else:
#         return render_template('query_group.html')