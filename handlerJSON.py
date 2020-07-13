from server import DBinterface as iDB
import datetime
from datetime import timezone
import ast
from server import ForAuthen as FA


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
            result = iDB.getMany(collectionName, filterJSON)
            # print(result)
            resultData = result
        elif methodJSON == "delete":
            parametrsMsg = msg["parametrs"]
            collectionName = parametrsMsg["collectionName"]
            filterJSON = parametrsMsg["filter"]
            result = iDB.deleteMany(collectionName, filterJSON)
            # print(result)
            resultData = result["n"]
        elif methodJSON == "put":
            parametrsMsg = msg["parametrs"]
            collectionName = parametrsMsg["collectionName"]
            dataJSON = parametrsMsg["data"]
            dataJSON["id"] = iDB.getLastId(collectionName) + 1
            dataJSON["Date"] = datetime.datetime.now(timezone.utc).isoformat(sep=" ")
            result = iDB.writeOne(collectionName, dataJSON).inserted_id
            # print(result)
            resultData = "ОК"
        elif methodJSON == "logIn":
            print(msg)
            parametrsMsg = msg["parametrs"]
            collectionName = parametrsMsg["collectionName"]
            login = parametrsMsg["name"]
            password = parametrsMsg["password"]
            result = FA.authen(login, password)
            print(result)
            resultData = result
        return responseJSON(resultData)
    except IndexError:
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

# loadMessage(msg1)
# loadMessage(msg2)
# loadMessage(msg3)
# loadMessage(msg4)
