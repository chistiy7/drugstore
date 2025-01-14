from datetime import date

from flask import Blueprint, session, redirect, url_for, current_app, request, render_template, flash
from database.insert import insert_one
from database.select import select_dict
from database.sql_provider import SQLProvider
import os
import re
from app.access import not_logged_in_required
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

blueprint_reg = Blueprint('reg_bp', __name__, template_folder='templates')

def is_valid_phone(phone):
    return re.fullmatch(r'^(?:\+7|8)\d{10}$', phone)

@blueprint_reg.route('/', methods=['GET', 'POST'])
@not_logged_in_required
def register():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            phone_num = request.form.get('phone_num')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if not username or not password or not confirm_password:
                flash("Все поля обязательны", "error")
                return redirect(url_for('reg_bp.register'))

            if password != confirm_password:
                flash("Пароли не совпадают", "error")
                return redirect(url_for('reg_bp.register'))
            if not is_valid_phone(phone_num):
                flash("Некорректный номер телефона","error")
                return redirect(url_for('reg_bp.register'))
            _sql = provider.get('user_exists.sql', e_username = username)
            result = select_dict(current_app.config['db_config'], _sql)
            user_count = result[0]['count'] if result else 0
            if user_count > 0:
                flash("Пользователь уже существует", "error")
                return redirect(url_for('reg_bp.register'))
            _sql = provider.get('register_user.sql', e_username = username, e_password = password, phone_num = phone_num, registration_date = date.today())
            print(_sql)
            success = insert_one(current_app.config['db_config'], _sql)

            if success:
                flash("Вы успешно зарегистрированы! Теперь войдите в систему.", "success")
                return redirect(url_for('auth_bp.auth_index'))
            else:
                flash("Ошибка при регистрации. Попробуйте позже.", "error")
                return redirect(url_for('reg_bp.register'))

    except Exception as e:
        print(f"Ошибка в register: {e}")
        flash("Ошибка сервера. Попробуйте позже.", "error")
        return redirect(url_for('reg_bp.register'))

    return render_template('register.html')