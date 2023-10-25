from fastapi import FastAPI
import psycopg2
from db import consts as db_consts

app = FastAPI()

pg_connection = psycopg2.connect(
    host=db_consts.DB_HOST,
    database=db_consts.DB,
    user=db_consts.DB_USER,
    password=db_consts.DB_PASSWORD)


@app.post("/get_layer_objects/")
def get_layer_objects(layer_id: int):
    """
    Функция возвращает объекто выбранного слоя
    :return:
    """
    # Open a cursor to perform database operations
    # print(request.data)
    cur = pg_connection.cursor()
    query = """
            SELECT geometry_object.id, data 
            FROM geometry_object JOIN layer 
            ON geometry_object.id=layer.id;
    """
    cur.execute(query)
    res = cur.fetchall()
    return res
