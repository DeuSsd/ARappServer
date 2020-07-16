# Тут будут храниться методы для работы с БД
from pymongo import MongoClient, results, cursor
import pymongo
from server.ForAuthen import coding

# подключаемся к базе данных MongoDB
client = MongoClient(port=27017)

# используем БД: ARdb
# db_data = client.ARdb
db = client.UserDB


# создание новой коллекции (добавление объекта )
def createNewObject(objectName):
    if not objectName in db.list_collection_names():
        db.create_collection(objectName)
        db.listOfObjects.insert_one({
            "id": getLastId("listOfObjects") + 1,
            "Name": objectName
        })
        return 'OK'


# метод возвращает новый ID физического объекта
def getLastId(collectionName):
    """
    вместо getNewId()
    :param collectionName:
    :return:
    """
    try:
        # вытаскивает все объекты из коллекции, забирает последнюю запись и вытаскивает из неё значение id
        thisCollection = db.get_collection(collectionName)
        return thisCollection.find(projection={'_id': False}).sort('id', pymongo.DESCENDING).limit(1)[0]["id"] + 1
    except KeyError:
        return 0
    except IndexError:
        return 0


# метод возвращает id коллекции физического объекта на вход его Name
def getIdOfCollection(objectName):
    return db.listOfObjects.find({"Name": objectName}, projection={'_id': False})[0]["id"]


# метод возвращает Name коллекции физического объекта на вход его id
def getNameOfCollection(objectId):
    return db.listOfObjects.find({"id": objectId}, projection={'_id': False})[0]["Name"]


# метод добавляет одну запись в коллекцию objectName
def writeOne(collectionName, data):
    thisCollection = db.get_collection(collectionName)
    return thisCollection.insert_one(data)


# метод возвращает  объект коллекции collectionName по фильтру filter
def getOne(collectionName, query=None):
    thisCollection = db.get_collection(collectionName)
    return thisCollection.find(query, projection={'_id': False}).limit(1)


# метод возвращает  объект коллекции collectionName по фильтру filter
def getMany(collectionName, query=None):
    thisCollection = db.get_collection(collectionName)
    return thisCollection.find(query, projection={'_id': False})


# метод возвращает последний объект коллекции collectionName
# TODO может быть стоит везде добавить возможность через атрибуты отключать ненужные поля
def getLastOne(collectionName):
    thisCollection = db.get_collection(collectionName)
    return thisCollection.find(projection={'_id': False, 'id': False}).sort('$natural', -1).limit(1)[0]


# метод возвращает объект коллекции collectionName по фильтру filter
def getOne(collectionName, query=None):
    thisCollection = db.get_collection(collectionName)
    return thisCollection.find_one(query, projection={'_id': False})[0]


# метод возвращает все объекты коллекции collectionName по фильтру filter
def getMany(collectionName, query=None, limit=0):
    thisCollection = db.get_collection(collectionName)
    result = []
    if limit:
        # limit is not good atribut
        # if limit > count(cursor)
        temporaryResult = []
        for object in thisCollection.find(query, projection={'_id': False}).sort('id', pymongo.DESCENDING).limit(limit):
            temporaryResult.append(object)
            i = 0
        for object in temporaryResult:
            result.append(temporaryResult[-1 - i])
            i += 1
    else:
        for object in thisCollection.find(query, projection={'_id': False}):
            result.append(object)
    return result


# метод удаляет один объект коллекции collectionName по фильтру filter
def deleteOne(collectionName, query):
    thisCollection = db.get_collection(collectionName)
    return thisCollection.delete_one(query).raw_result


# метод удаляет все объекты коллекции collectionName по фильтру filter
def deleteMany(collectionName, query):
    thisCollection = db.get_collection(collectionName)
    return thisCollection.delete_many(query).raw_result


# метод добавляет одну запись в коллекцию objectName
def writeOnewithshifr(id, name, password, code):
    sh_password = coding(password)
    db.users.insert_one({"id": id, "name": name, "password": sh_password, "code": code})


# проверка логина и пароля пользователя
def getNamefromlogin(login, password):
    print('login:', login,
         '\npassword: ', password)
    try:
        a = db.users.find({"name": login, "password": coding(password)})[0]["name"]
    except IndexError:
        a = "None"
    # except:
    #     print("Error")
    #TODO handle another except
    if a == login:
        a = "Successful authentication"
    else:
        a = "Incorrect login or password"
    #    if a == "true":
    #       print("Successful login and password")
    #    else:
    #        print("Incorrect login or password")
    return a


# метод возвращает password коллекции физического объекта на вход его id
def getPasswordOfCollection(objectId):
    return db.users.find({"id": objectId})[0]["password"]

# ////////////////////////////testing///////////////////////////////
# # writeOne("radiator",{"Name": "sds","DatTime":datetime.now()})
#
# # print(getOne("radiator",{"Temperature": {'$gt':80}}))
#
# collectionNames = "radiator"
# # while True:
# aa = getMany(collectionNames, {}, 110)
# print(aa)
# #     if not aa['n']: break
# print(getLastOne("radiator"))
# print(help(deleteOne(collectionNames,{"id":4})))
