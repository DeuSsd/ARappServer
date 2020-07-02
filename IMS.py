# Information and Measurement System

from pymongo import MongoClient
from datetime import datetime,timezone
import time

import DB as iDB

# import json

client = MongoClient(port=27017)
db = client.ARdb

f = open("data.txt", "r")
i = 1
while True:
    f.seek(0)  # возвращаемся в начало документа
    data = {"Temperature": round(float(f.read()), 2),
            "Date": datetime.now(timezone.utc)}  # формируем JSON объект, возможно нужно использовать JSON модуль
    # print(i,data)
    iDB.writeOne("radiator", data)  # добавляем одну запись в базу данных
    # time.sleep(1)
    # i+=1

#   datetime.fromisoformat(строка даты)
