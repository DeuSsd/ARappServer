# # Information and Measurement System
# from pymongo import MongoClient
# from datetime import datetime, timezone
# import time
# from ARappServer import DBinterface as iDB
#
# power = open("power.txt", "r")
# client = MongoClient(port=27017)
# db = client.ARdb
# collectionName = "radiator"
# f = open("data.txt", "r")
# objectId = iDB.AR_db.getLastId(collectionName)
# while True:
#     f.seek(0)  # возвращаемся в начало документа
#     power.seek(0)
#     objectId+=1
#     objectData = {
#         "id": objectId,
#         "temp1": round(float(f.read()), 3),
#         "powerStatus": power.read().strip() == "True",
#         "Date": datetime.now(timezone.utc).isoformat(sep=" ")
#     }
#     print(objectId, objectData)
#     iDB.AR_db.writeOne(collectionName, objectData)  # добавляем одну запись в базу данных
#     time.sleep(0.1)


import numpy as np
n = 5000
t = np.linspace(0,100.0,n)
X =  np.sin(t)
# X = (10*np.sin(t)+8*np.sin(0.5*t)+20*np.cos(0.2*t)-10*np.sin(0.8*t+2))
# Information and Measurement System
from pymongo import MongoClient
from datetime import datetime, timezone
import time
from ARappServer import DBinterface as iDB

power = open("power.txt", "r")
client = MongoClient(port=27017)
db = client.ARdb
collectionName = "radiator"
f = open("data.txt", "r")
objectId = iDB.AR_db.getLastId(collectionName)
for i in X:
    objectId+=1
    objectData = {
        "id": objectId,
        "temp1": round(float(i), 3),
        "powerStatus": power.read().strip() == "True",
        "Date": datetime.now(timezone.utc).isoformat(sep=" ")
    }
    print(objectId, objectData)
    iDB.AR_db.writeOne(collectionName, objectData)  # добавляем одну запись в базу данных
    # time.sleep(0.1)


