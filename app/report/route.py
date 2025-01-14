from flask import render_template, Blueprint, current_app, request, session
from database.select import select_dict, call_procedure
from app.access import group_required
from database.sql_provider import SQLProvider
import os


blueprint_report = Blueprint('report_bp', __name__, template_folder='templates')
report_list = [
    {'rep_id': '1', 'proc_name': 'product_report', 'sql': 'pharmacy.sql'},
    {'rep_id': '2', 'proc_name': 'staff_report', 'sql': 'user_report.sql'}
]

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/report_menu')
@group_required
def report_menu():
    return render_template('report_menu.html')


@blueprint_report.route('/report', methods=['POST'])
@group_required
def report():
    year = request.form['year']
    month = request.form['month']
    action = request.form['action']
    rep_id = int(request.form['rep']) - 1
    print("ОТЧЕТ АЙДИ-",rep_id)
    user_role = session.get('user_group')
    if action == 'report_view':
        return report_view(rep_id, year, month)
    elif action == 'report_create':
        if user_role != 'Manager':
            return 'У вас нет прав доступа на эту функциональность'
        return report_create(rep_id, year, month)


def report_view(rep_id, year, month):
    _sql = provider.get(report_list[rep_id]['sql'], e_month=month, e_year=year)
    print(_sql)
    result = select_dict(current_app.config['db_config'], _sql)
    if result:
        prod_title = f'Отчет'
        print(result)
        if rep_id == 0:
            return render_template('report_pharmacy.html', prod_title=prod_title, res=result, )
        else:
            return render_template('report_clients.html', prod_title=prod_title, res=result)
    else:
        return 'Результат не получен'


def report_create(rep_id, year, month):
    call_procedure(current_app.config['db_config'], report_list[rep_id]['proc_name'], month, year)
    return f'Отчет за {month}.{year} был создан.'