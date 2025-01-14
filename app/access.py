from functools import wraps
from flask import url_for, session, redirect, request, current_app

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('main_menu'))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            print(session['user_group'])
            user_role = session.get('user_group')
            user_request = request.endpoint # название blueprint + название обработчика
            print('request_endpoint=', user_request)
            user_bp = user_request.split('.')[0]
            user_obr = user_request.split('.')[1]
            access = current_app.config['db_access']
            print('access =', access)
            print('user_role =', user_role)
            print('user_bp =', user_bp)
            if user_role in access and (user_bp in access[user_role] or user_obr in access[user_role]):
                return func(*args, **kwargs)
            else:
                return 'У вас нет прав доступа на эту функциональность'
        else:
            return redirect(url_for('main_session'))
    return wrapper

def not_logged_in_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:  # Если пользователь уже авторизован
            return redirect(url_for('main_session'))  # Перенаправляем его в систему
        return func(*args, **kwargs)  # Иначе показываем страницу регистрации
    return wrapper
