import json
from werkzeug.utils import redirect
from query.route import blueprint_query
from auth.route import blueprint_auth
from report.route import blueprint_report
from registration.route import blueprint_reg
from basket.route_cache import blueprint_basket
from flask import Flask, render_template, session, url_for

app = Flask(__name__)

with open('../data/dbconfig.json') as f:
    app.config['db_config'] = json.load(f)

with open('../data/db_access.json') as f:
    app.config['db_access'] = json.load(f)

with open("../data/cache_config.json") as f:
    app.config['cache_config'] = json.load(f)

app.secret_key = 'You will never guess'

app.register_blueprint(blueprint_reg, url_prefix='/register')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_basket, url_prefix='/basket')


@app.route('/')
def main_session():
    if 'user_group' in session:
        user_role = session.get('user_group')
        message = f'Вы авторизованы как {user_role}'
        if user_role == 'Worker1' or user_role == 'Worker2':
            return render_template('main_menu_for_workers.html', message=message)
        if user_role == 'Client':
            return render_template('main_menu_for_clients.html', message=message)
        else:
            return render_template('main_menu.html', message=message)
    else:
        message = f'Вам необходимо авторизоваться'
    return render_template('login.html')


@app.route('/exit')
def exit_func():
    session.clear()
    return render_template('exit.html')
    #return redirect(url_for('main_session'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
