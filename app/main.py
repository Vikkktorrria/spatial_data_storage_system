from fastapi import FastAPI
import psycopg2
from db import consts as db_consts
import datetime
import requests

app = FastAPI()

pg_connection = psycopg2.connect(
    host=db_consts.DB_HOST,
    database=db_consts.DB,
    user=db_consts.DB_USER,
    password=db_consts.DB_PASSWORD)


def in_monitoring_system(in_date_time, f_name):
    print('in запрос отправлен', in_date_time, f_name)

    url = "http://monitoring-service-url"  # допустим, настоящий url
    message = {
        "date_time": in_date_time,
        "function": f_name,
    }
    response = requests.post(url, json=message)
    return response.status_code


def out_monitoring_system(out_date_time, f_name, status):
    print('out запрос отправлен', out_date_time, f_name, status)

    url = "http://monitoring-service-url"  # допустим, настоящий url
    message = {
        "date_time": out_date_time,
        "function": f_name,
        "status": status
    }
    response = requests.post(url, json=message)
    return response.status_code


def send_message(func):
    def wrapper(*args, **kwargs):
        in_monitoring_system(datetime.datetime.now(), func.__name__)
        result = func()
        out_monitoring_system(datetime.datetime.now(), func.__name__, 200)
        return result
    return wrapper


@send_message
@app.post("/get_layer_objects/")
def get_layer_objects(layer_id: int):
    """
    Функция возвращает объект выбранного слоя
    :return:
    """
    # Open a cursor to perform database operations
    cur = pg_connection.cursor()
    query = """
            SELECT geometry_object.id, data
            FROM geometry_object JOIN layer
            ON geometry_object.id=layer.id;
    """
    cur.execute(query)
    res = cur.fetchall()
    return res


