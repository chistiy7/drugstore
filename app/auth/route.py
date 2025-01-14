import hashlib
from hashlib import md5

from flask import Blueprint, session, redirect, url_for, current_app, request, render_template

from database.select import select_dict

blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')

@blueprint_auth.route('/', methods=['GET', 'POST'])
def auth_index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        _sql = f"""select id, user_role, user_name, pass from users
                       where user_name = '{username}'"""
        try:
            result = select_dict(current_app.config['db_config'], _sql)[0]
        except:
            return render_template('login.html', error="Неверный логин")
        if hashlib.md5(result['pass'].encode()).hexdigest() == hashlib.md5(password.encode()).hexdigest():
            user_group = result['user_role']
            user_id = int(result['id'])
            session['user_group'] = user_group
            session['user_id'] = user_id
            print('Выполнена аутентификация')
            return redirect(url_for('main_session'))
        else:
            return render_template('login.html', error="Неверный пароль")
            print("Неверный пароль")

    return render_template('login.html')

