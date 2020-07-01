# Тут будут храниться методы для работы с БД
from pymongo import MongoClient, collection
import pymongo

#для того, чтобы перевести строку в
import cPython

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

#new comment
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


# метод добавляет одну запись в коллекцию objectName
def writeOne(objectName, data):
    object = db.get_collection(objectName)
    object.insert_one(data)

# проверка логина и пароля пользователя
def getNamefromlogin(login, password):
    try:
        a= db.users.find({"name": login, "password": password})[0]["name"]
    except IndexError:
        a="a"
    if a==login:
        a="true"
    else:
        a="false"
    return a

#decode password
def decoding(password):
    from Cryptodome.Cipher import DES
    key = b'12345678'

    def pad(text):
        while len(text) % 8 != 0:
            text += b' '
        return text

    des = DES.new(key, DES.MODE_ECB)
    test_string = password
    text = bytes(test_string, 'utf-8')
    padded_text = pad(text)
    encrypted_text = des.encrypt(padded_text)
    print(encrypted_text)
    data = des.decrypt(encrypted_text)
    print(data)
    return encrypted_text

# testing
# writeOne("radiator",{"Name": "sds","DatTime":datetime.now()})
