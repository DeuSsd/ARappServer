# Тут будут храниться методы для работы с БД
from pymongo import MongoClient, collection
import pymongo
from ForAuthen import coding

from datetime import datetime

# подключаемся к базе данных MongoDB
client = MongoClient(port=27017)
# используем БД: ARdb
db = client.ARdb


# создание новой коллекции (добавление объекта )
def createNewObject(objectName):
    if not objectName in db.list_collection_names():
        db.create_collection(objectName)
        db.listOfObjects.insert_one({
            "id": getNewId(),
            "Name": objectName
        })
        return 'OK'

# метод возвращает новый ID физического объекта
def getNewId():
    # вытаскивает все объекты из коллекции, забирает последнюю запись и вытаскивает из неё значение id
    return db.listOfObjects.find().sort('id', pymongo.DESCENDING).limit(1)[0]["id"] + 1


# метод возвращает id коллекции физического объекта на вход его Name
def getIdOfCollection(objectName):
    return db.listOfObjects.find({"Name": objectName})[0]["id"]


# метод возвращает Name коллекции физического объекта на вход его id
def getNameOfCollection(objectId):
    return db.listOfObjects.find({"id": objectId})[0]["Name"]

# метод возвращает password коллекции физического объекта на вход его id
def getPasswordOfCollection(objectId):
    return db.users.find({"id": objectId})[0]["password"]

# метод добавляет одну запись в коллекцию objectName
def writeOne(objectName, data):
    object = db.get_collection(objectName)
    object.insert_one(data)

# метод добавляет одну запись в коллекцию objectName
def writeOnewithshifr(id, name, password, ph_num, code):
    sh_password=coding(password)
    db.users.insert_one({"id":id, "name":name, "password":sh_password, "ph_num":ph_num, "code":code})

# проверка логина и пароля пользователя
def getNamefromlogin(login, password):
    try:
        a= db.users.find({"name": login, "password": coding(password)})[0]["name"]
    except IndexError:
        a="a"
    if a==login:
        a="true"
    else:
        a="false"
    if a == "true":
        print("Successful login and password")
    else:
        print("Incorrect login or password")
    return a

# testing
# writeOne("radiator",{"Name": "sds","DatTime":datetime.now()})
