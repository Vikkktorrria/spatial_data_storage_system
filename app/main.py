from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import psycopg2
from db import consts as db_consts
import datetime
import requests
import time

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
    query = f"""
            SELECT geometry_object.id, ST_AsGeoJson(data)
            FROM geometry_object JOIN layer
            ON geometry_object.id=layer.id
            WHERE layer.id={layer_id};
            """
    cur.execute(query)
    res = cur.fetchall()

    layers_list = []
    for item in res:
        obj_id, obj_data = item
        obj_data = json.loads(obj_data)

        layers_list.append({
            'id': obj_id,
            'type': obj_data['type'],
            'coordinates': obj_data['coordinates'],
        })
    return JSONResponse({"layers": layers_list})


@send_message
@app.post("/get_layers/")
def get_layers():
    """
    Функция возвращает перечень слоёв
    :return:
    """
    cur = pg_connection.cursor()
    query = """
            SELECT *
            FROM layer;
    """
    cur.execute(query)
    res = cur.fetchall()
    return res


@send_message
@app.post("/export_spatial_data/")
def export_spatial_data():
    """
    Функция возвращает все пространственные данные из бд
    и передаёт их в систему экспорта пространственных данных
    :return:
    """



@send_message
@app.post("/export_table_data/")
def export_table_data():
    """
    Функция возвращает все табличные данные из бд
    и передаёт их в систему экспорта табличных данных
    :return:
    """

@send_message
@app.get("/import_spatial_data/")
def export_table_data():
    """
    Функция получает пространственные данные
    и сохраняет их в бд
    :return:
    """
    test_json = { "type": "Point",
    "coordinates": [30, 10]
    }
    query=f"INSERT INTO geometry_object(data, layer_id) VALUES (ST_GeomFromGeoJSON('{test_json}'), 1)"
