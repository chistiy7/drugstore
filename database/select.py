from calendar import month

from database.DBcm import DBContextManager


def select_list(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        try:
            print("ЗАПРОС ПОСЛЕ ПЕРЕДАЧИ В SELECT_LIST:",_sql)
            cursor.execute(_sql)
            result = cursor.fetchall()
            print("результат выполненния get:",result)
            schema = [item[0] for item in cursor.description]
        except:
            result = ()
            schema = []
    print("результат селект лист",result,schema)
    return result, schema


def select_dict(db_config: dict, _sql: str):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    print("~select.py/select_dict",result_dict)
    return result_dict


def call_procedure(db_config, procedure: str, month_arg, year_arg):
    with DBContextManager(db_config) as cursor:
        if cursor:
            proc_sql = f'CALL {procedure} ({month_arg}, {year_arg})'
            cursor.execute(proc_sql)
            result = cursor.fetchall()
            print(f'result: {result}')
            print(f'result: {result[0][0]}')
            if result[0][0] == 'exists':
                return f'Отчет за {month_arg}.{year_arg} уже существует'
            else:
                return f'Отчет за {month_arg}.{year_arg} создан'
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")