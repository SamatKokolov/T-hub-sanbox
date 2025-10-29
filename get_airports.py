import requests
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd

url = "https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/refs/heads/master/airports.json"
def parse_url_json(url):
    response = requests.get(url, timeout=30)
    api_data = response.json()      # применяем метод .json и передаем это значение переменной
    return api_data


"""Подключаемся к Postgres через docker container"""
def postgres_connect():
    load_dotenv()
    con = psycopg2.connect(
    dbname=os.getenv("dbname"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    host=os.getenv("host"),
    port=os.getenv("port")
    )
    return con


"""Функция создания таблицы"""
def create_table(cur, con):
    cur.execute(
        """CREATE TABLE IF NOT EXISTS airports(
        iata VARCHAR(50),
        lon VARCHAR(50),
        iso VARCHAR(50),
        status INTEGER,
        name VARCHAR(100),
        continent VARCHAR(50),
        type VARCHAR(50),
        lat VARCHAR(50),
        size VARCHAR(50));"""
        )
    con.commit()

"""Функция вставки данных из url в таблицу"""
def insert_into(cur, con):
    for data in parse_url_json(url):
        cur.execute(
        """INSERT INTO airports (iata, lon, iso, status, name, continent, type, lat, size)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            [data.get("iata"),
             data.get("lon"),
             data.get("iso"),
             data.get("status"),
             data.get("name"),
             data.get("continent"),
             data.get("type"),
             data.get("lat"),
             data.get("size")])
        con.commit()

def pandas_head(con, num):
    sql = "SELECT * FROM airports"
    query = pd.read_sql_query(sql, con)
    print(query.head(num))

def main():
    with postgres_connect() as con:
        cur = con.cursor()
    create_table(cur, con)
    cur.execute(
        """SELECT count(*)
        FROM airports"""
    )
    if cur.fetchone()[0] == 0:
        insert_into(cur, con)
    with pd.option_context("display.max_columns", None, "display.width", 1000):
        pandas_head(con, 20)



