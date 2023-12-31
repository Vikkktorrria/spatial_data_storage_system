from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
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


def in_monitoring_system(in_date_time: datetime.datetime, f_name: str):
    """
    Функция, предназначенная для вызова системы мониторинга
     и передачи сообщения о входящем запросе
     со следующими параметрами:
    :param in_date_time: время поступления запроса
    :param f_name: название функции
    :return:
    """
    print('in запрос отправлен', in_date_time, f_name)

    url = "http://monitoring-service-url/some_function"  # допустим, настоящий url
    message = {
        "date_time": str(in_date_time),
        "function": f_name,
    }
    print(message)
    response = requests.post(url, json=message)
    return response.status_code


def out_monitoring_system(out_date_time: datetime.datetime, f_name: str, status: str):
    """
    Функция, предназначенная для вызова системы мониторинга
    и передачи сообщения о результате выполнения функции
    со следующими параметрами:
    :param out_date_time: время завершения работы функции
    :param f_name: название функции
    :param status: статус, с которым завершилась функция (сейчас это ok, error)
    :return:
    """
    print('out запрос отправлен', out_date_time, f_name, status)

    url = "http://monitoring-service-url/some_function"  # допустим, настоящий url
    message = {
        "date_time": str(out_date_time),
        "function": f_name,
        "status": status
    }
    print(message)
    response = requests.post(url, json=message)
    return response.status_code


def send_message(func):
    """
    Декоратор,
    вызывает функцию in_monitoring_system до выполнения основной функции,
    затем функцию out_monitoring_system после выполнения
    """

    def wrapper(*args, **kwargs):
        in_monitoring_system(datetime.datetime.now(), func.__name__)
        try:
            result = func()
            out_monitoring_system(datetime.datetime.now(), func.__name__, 'ok')
            return result
        except:
            out_monitoring_system(datetime.datetime.now(), func.__name__, 'error')

    return wrapper


@send_message
@app.get("/get_layers/")
def get_layers():
    """
    Функция возвращает перечень слоёв
    :return:
    {
      "layers": [
          {
            "id": идентификатор_слоя,
            "name": "ИмяСлоя"
          },
          {
            "id": идентификатор_слоя,
            "name": "ИмяСлоя"
          },
          ...
          {
            "id": идентификатор_слоя,
            "name": "ИмяСлоя"
          }
      ]
    }
    """
    cur = pg_connection.cursor()
    query = """
            SELECT *
            FROM layer;
    """
    cur.execute(query)
    res = cur.fetchall()
    layers_list = []
    for layer in res:
        layer_id, layer_name = layer
        layers_list.append({
            'id': layer_id,
            'name': layer_name
        })
    return JSONResponse({"layers": layers_list})


@send_message
@app.get("/get_layer_objects/")
def get_layer_objects(layer_id: int):
    """
    Функция возвращает объекты выбранного слоя
    :return:
    {
        "objects": [
            {
                "id": идентификатор_объекта,
                "type": "ТипОбъекта (Point, LineString, Polygon)",
                "coordinates": [координаты]
            },
            ...
            {
                "id": идентификатор_объекта,
                "type": "ТипОбъекта (Point, LineString, Polygon)",
                "coordinates": [координаты]
            }
        ]
    }
    """
    cur = pg_connection.cursor()
    query = f"""
            SELECT geometry_object.id, ST_AsGeoJson(data)
            FROM geometry_object JOIN layer
            ON geometry_object.layer_id=layer.id
            WHERE layer.id={layer_id};
            """
    cur.execute(query)
    res = cur.fetchall()

    objects_list = []
    for item in res:
        obj_id, obj_data = item
        obj_data = json.loads(obj_data)

        objects_list.append({
            'id': obj_id,
            'type': obj_data['type'],
            'coordinates': obj_data['coordinates'],
        })
    return JSONResponse({
        "objects": objects_list
    })


@send_message
@app.get("/export_spatial_data/")
def export_spatial_data(layer_id: int):
    """
    Функция возвращает все пространственные данные по определённому слою
    и передаёт их в систему экспорта пространственных данных
    :return:
    JSON следующей структуры
    {
        "layer_id": идентификатор_слоя
        "layer_name": "ИмяСЛоя",
        "objects": [
            {
                "id": идентификатор_объекта,
                "type": "ТипОбъекта (Point, LineString, Polygon)",
                "coordinates": [координаты]
            },
            {
                ...
            }
        ]
    }
    """
    cur = pg_connection.cursor()
    query = f"""
            SELECT geometry_object.id AS geom_obj_id, layer.id AS layer_id, layer.name, ST_AsGeoJson(data)
            FROM geometry_object JOIN layer
            ON geometry_object.layer_id=layer.id
            WHERE layer.id = {layer_id};
    """
    cur.execute(query)
    res = cur.fetchall()
    objects = []
    layer_name = ''
    for result in res:
        geom_obj_id, layer_id, layer_name, geojson_string = result
        geojson_data = json.loads(geojson_string)

        objects.append({
            'id': geom_obj_id,
            'type': geojson_data['type'],
            'coordinates': geojson_data['coordinates']
        })

    return JSONResponse({
        "layer_id": layer_id,
        "layer_name": layer_name,
        "objects": objects
    })


@send_message
@app.get("/export_table_data/")
def export_table_data(layer_id: int):
    """
    Функция возвращает табличные данные по слою
    и передаёт их в систему экспорта табличных данных
    :return:
    {
      "layer_name": "ИмяСлоя",
      "layer_color": "цвет",
      "objects": [
        {
          "id": идентификатор_объекта,
          "color": "цвет"
        }
      ]
    }
    """
    cur = pg_connection.cursor()
    get_layers_styles_query = f"SELECT layer.name, color " \
                              f"FROM layers_style " \
                              f"JOIN layer ON layers_style.layer_id=layer.id " \
                              f"WHERE layer.id={layer_id};"
    cur.execute(get_layers_styles_query)
    res1 = cur.fetchall()

    if res1 == []:
        return JSONResponse({})

    layer_name, layer_color = res1[0]

    get_objects_styles_query = f"SELECT objects_style.object_id, color " \
                               f"FROM objects_style JOIN geometry_object " \
                               f"ON objects_style.object_id=geometry_object.id " \
                               f"WHERE geometry_object.layer_id={layer_id};"
    cur.execute(get_objects_styles_query)
    res2 = cur.fetchall()
    objects_json = []
    for item in res2:
        obj_id, obj_color = item
        objects_json.append({
            'id': obj_id,
            'color': obj_color,
        })

    return JSONResponse({
        "layer_name": layer_name,
        "layer_color": layer_color,
        "objects": objects_json
    })


@send_message
@app.get("/export_all_spatial_data/")
def export_all_spatial_data():
    """
    Функция возвращает все пространственные данные из бд
    и передаёт их в систему экспорта пространственных данных
    :return:
    JSON следующей структуры
    {
      "layers": [
        {
          "id": идентификатор_слоя,
          "name": "имя_слоя",
          "objects": [
            {
              "id": идентификатор_объекта,
              "type": "ТипОбъекта (Point, LineString, Polygon)",
              "coordinates": [x, y]
            }
          ]
        }
      ]
    }
    """
    cur = pg_connection.cursor()
    query = """
            SELECT geometry_object.id AS geom_obj_id, layer.id AS layer_id, layer.name, ST_AsGeoJson(data)
            FROM geometry_object JOIN layer
            ON geometry_object.layer_id=layer.id;
    """
    cur.execute(query)
    res = cur.fetchall()
    layer_objects = []

    for result in res:
        geom_obj_id, layer_id, layer_name, geojson_string = result
        geojson_data = json.loads(geojson_string)

        layer = next((layer for layer in layer_objects if layer['id'] == layer_id), None)
        if layer:
            layer['objects'].append({
                'id': geom_obj_id,
                'type': geojson_data['type'],
                'coordinates': geojson_data['coordinates']
            })
        else:
            layer_objects.append({
                'id': layer_id,
                'name': layer_name,
                'objects': [{
                    'id': geom_obj_id,
                    'type': geojson_data['type'],
                    'coordinates': geojson_data['coordinates']
                }]
            })
    return JSONResponse({"layers": layer_objects})


@send_message
@app.get("/export_all_table_data/")
def export_all_table_data():
    """
    Функция возвращает все табличные данные из бд
    и передаёт их в систему экспорта табличных данных
    :return:
    {
      "layers": [
        {
          "id": идентификатор_слоя,
          "name": "ИмяСлоя",
          "color": "цвет"
        },
        ...
        {
          "id": идентификатор_слоя,
          "name": "ИмяСлоя",
          "color": "цвет"
        }
      ],
      "objects": [
        {
          "id": идентификатор_объекта,
          "color": "цвет"
        },
        ...
        {
            ...
        }
      ]
    }
    """
    cur = pg_connection.cursor()
    get_layers_styles_query = "SELECT layers_style.layer_id, layer.name, color " \
                              "FROM layers_style " \
                              "JOIN layer ON layers_style.layer_id=layer.id;"
    cur.execute(get_layers_styles_query)
    res1 = cur.fetchall()
    layers_json = []

    for item in res1:
        layer_id, layer_name, layer_color = item
        layers_json.append({
            'id': layer_id,
            'name': layer_name,
            'color': layer_color,
        })

    get_objects_styles_query = "SELECT objects_style.object_id, color " \
                               "FROM objects_style JOIN geometry_object " \
                               "ON objects_style.object_id=geometry_object.id;"
    cur.execute(get_objects_styles_query)
    res2 = cur.fetchall()
    objects_json = []
    for item in res2:
        obj_id, obj_color = item
        objects_json.append({
            'id': obj_id,
            'color': obj_color,
        })

    return JSONResponse({
        "layers": layers_json,
        "objects": objects_json
    })

# @send_message
# @app.post("/import_spatial_data/")
# def import_spatial_data():
#     """
#     Функция получает пространственные данные
#     и сохраняет их в бд
#     :return:
#     {
#         "layer_name":layer_name,
#         "objects":[
#             {
#                 "type":object_type,
#                 "coordinates":object_coordinates
#             },
#             …
#             {
#                 "type":object_type,
#                 "coordinates":object_coordinates
#             }
#         ]
#     }
#     """
#     url = "http://example.com/your_external_service_endpoint"
#     response = requests.get(url)
#     data = response.json()
