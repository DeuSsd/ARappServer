# Information and Measurement System
from pymongo import MongoClient
from datetime import datetime, timezone
import time
from server import DBinterface as iDB

client = MongoClient(port=27017)
db = client.ARdb

collectionName = "radiator"
f = open("data.txt", "r")
objectId = iDB.getLastId(collectionName)
while True:
    f.seek(0)  # возвращаемся в начало документа
    objectId+=1
    objectData = {
        "id": objectId,
        "Temperature": round(float(f.read()), 3),
        "Date": datetime.now(timezone.utc).isoformat(sep=" ")
    }
    print(objectId, objectData)
    iDB.writeOne(collectionName, objectData)  # добавляем одну запись в базу данных
    time.sleep(0.1)
