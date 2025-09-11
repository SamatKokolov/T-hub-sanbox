import requests
import psycopg2


response = requests.get("https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/refs/heads/master/airports.json")
api_data = response.json()      # применяем метод .json и передаем это значение переменной

"""Подключаемся к Postgres через docker container"""
con = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5433"
)

cur = con.cursor()
"""Создаем таблицу"""
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

"""Задаем условие, если таблица пустая, то добавляем значения"""
cur.execute(
    """SELECT *
    FROM airports"""
)
if cur.fetchall() == []:
    for d in api_data:
        cur.execute(
        """INSERT INTO airports (iata, lon, iso, status, name, continent, type, lat, size)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", [d.get("iata"), d.get("lon"), d.get("iso"), d.get("status"), d.get("name"), d.get("continent"), d.get("type"), d.get("lat"), d.get("size")])
        con.commit()

cur.execute(
    """SELECT *
    FROM airports
    LIMIT 20;"""
)
print(cur.fetchall())
con.cancel()


