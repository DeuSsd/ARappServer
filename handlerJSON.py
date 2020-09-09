from server import DBinterface as iDB
import datetime
from datetime import timezone
import ast
from server import Authentification as FA
import base64
from Crypto.PublicKey import RSA



def loadMessage(msg):
    """
    Данный метод принимает на вход сообщение (msg) типа str, которое
    является запросом, содержит JSON файл,
    в случае языка Python не работаем с типом JSON  непосредственно,
    т.к. имеется встроенный тип dict отлично подходит для его замены.
    (Далее JSON == dict)
    После процедуры парсинга, извлкекаем хранящяяся параметры
    и вызываем нужный обработчик в зависимоти от параметра 'method'

    Вид JSON запроса:
    {
        "method": "вид метода",
        "parametrs": {
            "collectionName": "Имя необходимой коллекции",
            "filter": {}
        }
    }

    Вид JSON ответа:
    {
        "method": "response",
        "data": {}
        }
    }
    Доступные методы:
        'get':
            запрос на получение данных из коллекции "collectionName",
            удовлетворяющих фильтру "filter";
        put:
            запрос на добавление данных "data"
            в коллекцию "collectionName";
        delete:
            запрос на удаление данных из коллекции "collectionName",
            удовлетворяющих фильтру "filter";
        getLastData:
            запрос почледней строки данных из коллекции (дан id физического объекта)
        authen:
            запрос на уйтентификацию пользователя
            (проверка логина и пароля на соответствие);

    :param msg: запрос от клиента, который нужно обработать - тип str
    :return: ответ с сервера в виде сообщения типа str, которое содержит JSON объект
            на результат выполнения запроса.
    """
    try:
        msg = ast.literal_eval(msg)
        methodJSON = msg["method"]
        if methodJSON == "get":
            parametrsMsg = msg["parametrs"]
            collectionName = parametrsMsg["collectionName"]
            filterJSON = parametrsMsg["filter"]
            result = iDB.AR_db.getMany(collectionName, filterJSON)
            # print(result)
            resultData = result
        elif methodJSON == "delete":
            parametrsMsg = msg["parametrs"]
            collectionName = parametrsMsg["collectionName"]
            filterJSON = parametrsMsg["filter"]
            result = iDB.AR_db.deleteMany(collectionName, filterJSON)
            # print(result)
            resultData = result["n"]

        elif methodJSON == "put":
            parametrsMsg = msg["parametrs"]
            collectionName = parametrsMsg["collectionName"]
            dataJSON = parametrsMsg["data"]
            dataJSON["id"] = iDB.AR_db.getLastId(collectionName) + 1
            dataJSON["Date"] = datetime.datetime.now(timezone.utc).isoformat(sep=" ")
            result = iDB.AR_db.writeOne(collectionName, dataJSON).inserted_id
            # print(result)
            resultData = "ОК"


        elif methodJSON == "getLast":
            parametrsMsg = msg["parametrs"]
            collectionId = int(parametrsMsg["ObjectID"])
            result = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(collectionId))
            resultData = result


        # elif methodJSON == "getLastData":
        #     collectionId = int(msg["ObjectID"])
        #     result = iDB.getLastOne(iDB.getNameOfCollection(collectionId))
        #     resultData = result

        elif methodJSON == "logIn":
            # print(msg)
            parametrsMsg = msg["parametrs"]
            # collectionName = parametrsMsg["collectionName"]
            collectionName = "users"
            login = parametrsMsg["name"]
            password_b64 = parametrsMsg["password"]
            password = base64.b64decode(password_b64)
            result = FA.authen(login, password)
            resultData = result

        elif methodJSON == "getPublicKey":
            f = open('publickey.xml')
            #print(f.read())
            resultData = f

        elif methodJSON == "getLast":
            parametrsMsg = msg["parametrs"]
            collectionId = int(parametrsMsg["ObjectID"])
            result = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(collectionId))
            resultData = result

        elif methodJSON == "getWarning":
            parametrsMsg = msg["parametrs"]
            collectionId = int(parametrsMsg["ObjectID"])
            if collectionId == 1:
                result = str("Only the temperature sensor works!")
            else:
                result = str("Empty")
            resultData = result

        # elif methodJSON == "getLastData":
        #     collectionId = int(msg["ObjectID"])
        #     result = iDB.getLastOne(iDB.getNameOfCollection(collectionId))
        #     resultData = result

        elif methodJSON == "getPublicKey":
            key = RSA.importKey(open('publickey.pem').read())
            key.export_key()
            resultData= str(key.export_key())

        else:
            resultData = "Wrong Method"
        return responseJSON(resultData)
    except StopIteration:
        resultData = "Wrong Request"
        return responseJSON(resultData)



# ответ на запрос
def responseJSON(data):
    """
    Формирует из данных "data" ответ клиенту
    :param data: принимает на вхлд двнные, которые нужно передать тип str с JSON объектом внутри
    :return: сформированное сообщение, готовое к отправке клиенту
    """
    msg = {}
    msg["method"] = "response"
    msg["data"] = data
    return msg

# /////////////////test/////////////////
# msg1 = {
#     "method": "get",
#     "parametrs": {
#         "collectionName": "radiator",
#         "filter": {
#             "Temperature": {'$gt': 90}
#         }
#     }
# }
#
# msg2 = {
#     "method": "delete",
#     "parametrs": {
#         "collectionName": "radiator",
#         "filter": {
#             "Temperature": {'$lt': 0}
#         }
#     }
# }
#
# msg3 = {
#     "method": "put",
#     "parametrs": {
#         "collectionName": "radiator",
#         "data": {
#             "Temperature": 150.256
#         }
#     }
# }
#
# msg4 = {
#     "method": "get",
#     "parametrs": {
#         "collectionName": "radiator",
#         "filter": {
#             "Temperature": {'$gt': 150}
#         }
#     }
# }
#
# msg5 = {
#     "method" : "getLastData",
#     "ObjectID": 1
# }
# loadMessage(msg1)
# loadMessage(msg2)
# loadMessage(msg3)
# print(loadMessage(str(msg5)))

