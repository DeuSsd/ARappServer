# Тут будут храниться методы для работы с БД
from pymongo import MongoClient, results, cursor
import pymongo

import ARappServer.encryptionDES as encDES

# подключаемся к базе данных MongoDB
client = MongoClient(port=27017)

# используем БД: ARdb, UserDB
# db_data = MongoClient.ARdb
# db = MongoClient.UserDB

DB_DATA = "ARdb"
DB_USERS = "UserDB"


class BaseDBinterface:
    def __init__(self, DBname):
        """Constructor"""
        self.db = self._get_db_object(DBname)

    # def __get_db(self):
    #     return self._db

    # @property
    # def get_db(self):
    #     #TODO fix this, becouse we already have self.__get_db()
    #     return self.__get_db()

    def _get_list_db_names(self):
        # TODO modify
        result = []
        # temporary_result = []
        for item in MongoClient().list_database_names():
            result.append(item)
        # for i in enumerate(temporary_result):
        #     result.append(temporary_result[-1 - i[0]])
        return result

    def _get_db_object(self, database_name):
        # TODO modify
        array = self._get_list_db_names()
        if database_name in array:
            return MongoClient().get_database(database_name)
        else:
            return None

    # метод добавляет одну запись в коллекцию collection_name
    def writeOne(self, collection_name, data):
        this_collection = self.db.get_collection(collection_name)
        return this_collection.insert_one(data)

    # метод возвращает объект коллекции collection_name по фильтру filter
    def getOne(self, collection_name, query=None):
        this_collection = self.db.get_collection(collection_name)
        return this_collection.find_one(query, projection={'_id': False})[0]

    # метод возвращает все объекты коллекции collection_name по фильтру filter
    def getMany(self, collection_name, query=None, limit=0):
        this_collection = self.db.get_collection(collection_name)
        result = []
        if limit:
            # limit is not good atribut
            # if limit > count(cursor)
            temporary_result = []
            for item in this_collection.find(query, projection={'_id': False}).sort('id', pymongo.DESCENDING).limit(
                    limit):
                temporary_result.append(item)
            # i = 0
            for i in enumerate(temporary_result):
                result.append(temporary_result[-1 - i[0]])
                # i += 1
        else:
            for item in this_collection.find(query, projection={'_id': False}):
                result.append(item)
        return result

    # # метод возвращает  объект коллекции collection_name по фильтру filter
    # def getOne(self, collection_name, query=None):
    #     this_collection = self.db.get_collection(collection_name)
    #     return this_collection.find(query, projection={'_id': False}).limit(1)
    #
    # # метод возвращает  объект коллекции collection_name по фильтру filter
    # def getMany(self, collection_name, query=None):
    #     this_collection = self.db.get_collection(collection_name)
    #     return this_collection.find(query, projection={'_id': False})

    # метод возвращает последний объект коллекции collection_name
    # TODO может быть стоит везде добавить возможность через атрибуты отключать ненужные поля
    def getLastOne(self, collection_name):
        this_collection = self.db.get_collection(collection_name)
        return this_collection.find(projection={'_id': False, 'id': False}).sort('$natural', -1).limit(1)[0]

    # метод удаляет один объект коллекции collection_name по фильтру filter
    def deleteOne(self, collection_name, query):
        this_collection = self.db.get_collection(collection_name)
        return this_collection.delete_one(query).raw_result

    # метод удаляет все объекты коллекции collection_name по фильтру filter
    def deleteMany(self, collection_name, query):
        this_collection = self.db.get_collection(collection_name)
        return this_collection.delete_many(query).raw_result

    # создаёт новую коллекцию, если таковой ещё нет в БД
    def create_new_collection(self, object_name):
        if not object_name in self.db.list_collection_names():
            return self.db.create_collection(object_name)

    # метод возвращает новый ID физического объекта
    def getLastId(self, collection_name):
        """
        вместо getNewId()
        :param collection_name:
        :return:
        """
        try:
            # вытаскивает все объекты из коллекции, забирает последнюю запись и вытаскивает из неё значение id
            this_collection = self.db.get_collection(collection_name)
            return this_collection.find(projection={'_id': False}).sort('id', pymongo.DESCENDING).limit(1)[0]["id"]
        except KeyError:
            return 0
        except IndexError:
            return 0


class ArDB(BaseDBinterface):

    # создание новой коллекции (добавление объекта )
    def createNewObject(self, object_name):
        if self.create_new_collection(object_name):
            self.db.listOfObjects.insert_one({
                "id": self.getLastId("listOfObjects") + 1,
                "Name": object_name
            })
            return 'OK'

    # метод возвращает id коллекции физического объекта на вход его Name
    def getIdOfCollection(self, objectName):
        return self.db.listOfObjects.find({"Name": objectName}, projection={'_id': False})[0]["id"]

    # метод возвращает Name коллекции физического объекта на вход его id
    def getNameOfCollection(self, objectId):
        return self.db.listOfObjects.find({"id": objectId}, projection={'_id': False})[0]["Name"]


class UserDB(BaseDBinterface):

    #запись
    def writeOnewithshifr(self, id, name, password, code):
        sh_password = encDES.coding(password)
        self.db.users.insert_one({"id": id, "name": name, "password": sh_password, "code": code})

    # проверка логина и пароля пользователя
    def getNamefromlogin(self, login, password):
        # print('login:', login,
        #       '\npassword: ', password)
        try:
            result_message = self.db.users.find({"name": login, "password": encDES.coding(password)})[0]["name"]
        except IndexError:
            result_message = "None"
        # except:
        #         #     print("Error")
        #         # TODO handle another except

        if result_message == login:
            result_message = "Successful authentification"
        else:
            result_message = "Incorrect login or password"
        return result_message

    # метод возвращает password коллекции физического объекта на вход его id
    def getPasswordOfCollection(self, objectId):
        return self.db.users.find({"id": objectId})[0]["password"]


AR_db = ArDB(DB_DATA)
User_DB = UserDB(DB_USERS)

# ////////////////////////////testing///////////////////////////////
# writeOne("radiator",{"Name": "sds","DatTime":datetime.now()})

# print(getOne("radiator",{"Temperature": {'$gt':80}}))

if __name__ == '__main__':
# collection_names = "radiator"
# # while True:
# aa = getMany(collection_names, {}, 110)
# print(aa)
# #     if not aa['n']: break
# print(getLastOne("radiator"))
# print(help(deleteOne(collection_names,{"id":4})))

# DB = BaseDBinterface(client.ARdb)
# DB1 = User_DB(client.UserDB)
# print(ArDB("ARdb").getMany("radiator",query={"Temperature": {'$lt': 100}}))
# print(DB1.getLastId('users'))
# print(bool(get_db("ARdb")))
# print(UserDB(DB_USERS).getNamefromlogin("T/EST", "TEST0912375981237059812730"))
    print(AR_db.createNewObject("radiator"))
    print(User_DB.writeOnewithshifr(1,"Roman","qwer1ty12","one"))
# print(AR_DB("ARdb").get_db())
# print(MongoClient().ARdb)

