from ARappServer import DBinterface as iDB
import datetime
from datetime import timezone
import ast
from ARappServer import Authentification as FA
import base64
from Crypto.PublicKey import RSA

import xml.etree.ElementTree as ET
from json2xml import json2xml
import xmltodict

from json2xml.utils import readfromurl, readfromstring, readfromjson
from io import BytesIO

from ARappServer.GetPrognose import prognos



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
        logIn:
            запрос на аутентификацию пользователя
            (проверка логина и пароля на соответствие);

    :param msg: запрос от клиента, который нужно обработать - тип str
    :return: ответ с сервера в виде сообщения типа str, которое содержит JSON объект
            на результат выполнения запроса.
    """
    try:
        # old
        # msg = ast.literal_eval(msg)
        # methodJSON = msg["method"]
        # if methodJSON == "get":
        #     parametrsMsg = msg["parametrs"]
        #     collectionName = parametrsMsg["collectionName"]
        #     filterJSON = parametrsMsg["filter"]
        #     result = iDB.AR_db.getMany(collectionName, filterJSON)
        #     # print(result)
        #     resultData = result

        # elif methodJSON == "getLast":
        #     parametrsMsg = msg["parametrs"]
        #     collectionId = int(parametrsMsg["ObjectID"])
        #     result = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(collectionId))
        #     resultData = result
        #

        # elif methodJSON == "delete":
        #     parametrsMsg = msg["parametrs"]
        #     collectionName = parametrsMsg["collectionName"]
        #     filterJSON = parametrsMsg["filter"]
        #     result = iDB.AR_db.deleteMany(collectionName, filterJSON)
        #     # print(result)
        #     resultData = result["n"]
        #
        # elif methodJSON == "put":
        #     parametrsMsg = msg["parametrs"]
        #     collectionName = parametrsMsg["collectionName"]
        #     dataJSON = parametrsMsg["data"]
        #     dataJSON["id"] = iDB.AR_db.getLastId(collectionName) + 1
        #     dataJSON["Date"] = datetime.datetime.now(timezone.utc).isoformat(sep=" ")
        #     result = iDB.AR_db.writeOne(collectionName, dataJSON).inserted_id
        #     # print(result)
        #     resultData = "ОК"
        #
        #
        # elif methodJSON == "getLast":
        #     parametrsMsg = msg["parametrs"]
        #     collectionId = int(parametrsMsg["ObjectID"])
        #     result = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(collectionId))
        #     resultData = result
        #
        #
        # # elif methodJSON == "getLastData":
        # #     collectionId = int(msg["ObjectID"])
        # #     result = iDB.getLastOne(iDB.getNameOfCollection(collectionId))
        # #     resultData = result
        #
        # elif methodJSON == "logIn":
        #     # print(msg)
        #     parametrsMsg = msg["parametrs"]
        #     # collectionName = parametrsMsg["collectionName"]
        #     collectionName = "users"
        #     login = parametrsMsg["name"]
        #     password_b64 = parametrsMsg["password"]
        #     password = base64.b64decode(password_b64)
        #     result = FA.authen(login, password)
        #     resultData = result
        #
        # elif methodJSON == "getLast":
        #     parametrsMsg = msg["parametrs"]
        #     collectionId = int(parametrsMsg["ObjectID"])
        #     result = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(collectionId))
        #     resultData = result
        #
        # elif methodJSON == "getWarning":
        #     parametrsMsg = msg["parametrs"]
        #     collectionId = int(parametrsMsg["ObjectID"])
        #     if collectionId == 1:
        #         result = str("Only the temperature sensor works!")
        #     else:
        #         result = str("Empty")
        #     resultData = result
        #
        # # elif methodJSON == "getLastData":
        # #     collectionId = int(msg["ObjectID"])
        # #     result = iDB.getLastOne(iDB.getNameOfCollection(collectionId))
        # #     resultData = result
        #
        # elif methodJSON == "getPublicKey":
        #     key = RSA.importKey(open('publickey.pem').read())
        #     key.export_key()
        #     resultData= str(key.export_key())
        #
        # else:
        #     resultData = "Wrong Method"

        # new
        msgXML = ET.fromstring(msg)
        method_msg = msgXML.find("method").text
        parametrs_msg = msgXML.find("parameters")
        print(method_msg)
        if method_msg == "getLast":
            collectionId = int(parametrs_msg.find("ObjectID").text)
            result = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(collectionId))
            # print(result)
            result = json2xml.Json2xml(result,attr_type=False).to_xml()  # JSON -> XML string
            # print(result)
            resultData = ET.fromstring(result)  # XML string -> XML
            # print(resultData)

        # if methodJSON == "get":
        #     parametrsMsg = msg["parametrs"]
        #     collectionName = parametrsMsg["collectionName"]
        #     filterJSON = parametrsMsg["filter"]
        #     result = iDB.AR_db.getMany(collectionName, filterJSON)
        #     # print(result)
        #     resultData = result

        # elif methodJSON == "delete":
        #     parametrsMsg = msg["parametrs"]
        #     collectionName = parametrsMsg["collectionName"]
        #     filterJSON = parametrsMsg["filter"]
        #     result = iDB.AR_db.deleteMany(collectionName, filterJSON)
        #     # print(result)
        #     resultData = result["n"]
        #
        # elif methodJSON == "put":
        #     parametrsMsg = msg["parametrs"]
        #     collectionName = parametrsMsg["collectionName"]
        #     dataJSON = parametrsMsg["data"]
        #     dataJSON["id"] = iDB.AR_db.getLastId(collectionName) + 1
        #     dataJSON["Date"] = datetime.datetime.now(timezone.utc).isoformat(sep=" ")
        #     result = iDB.AR_db.writeOne(collectionName, dataJSON).inserted_id
        #     # print(result)
        #     resultData = "ОК"
        #
        #
        # elif methodJSON == "getLast":
        #     parametrsMsg = msg["parametrs"]
        #     collectionId = int(parametrsMsg["ObjectID"])
        #     result = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(collectionId))
        #     resultData = result
        #
        #
        # # elif methodJSON == "getLastData":
        # #     collectionId = int(msg["ObjectID"])
        # #     result = iDB.getLastOne(iDB.getNameOfCollection(collectionId))
        # #     resultData = result

        elif method_msg == "logIn":
            print(method_msg)
            # collectionName = "users"
            login = parametrs_msg.find("login").text
            print(parametrs_msg,login)
            password_b64 = parametrs_msg.find("password").text
            password = base64.b64decode(password_b64)
            result = ET.Element('result')
            result.text = FA.authen(login, password)
            resultData = result

        elif method_msg == "getBuildSettings":
            ObjectId = int(parametrs_msg.find("ObjectID").text)
            objectsBuildSettings = iDB.AR_db.getObjectBuildSettings(ObjectId)

            objectsSettings = {}
            index = 1
            for item in objectsBuildSettings:
                objectsSettings["object"+str(index)] = item
                index+=1
            objectsSettings = json2xml.Json2xml(objectsSettings,attr_type=False).to_xml()  # JSON -> XML string
            objectsSettings = ET.fromstring(objectsSettings)
            objectsSettings.tag = "objectsSettings"
            data = ET.Element("data")
            data.append(objectsSettings)
            initialData = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(ObjectId))
            # print(result)
            initialData = json2xml.Json2xml(initialData, attr_type=False).to_xml()  # JSON -> XML string
            # print(result)
            initialData = ET.fromstring(initialData)
            initialData.tag = "initialData"
            data.append(initialData)
            resultData = data  # XML string -> XML
            # tree = ET.parse('BuildSettings.xml')
            # root = tree.getroot()
            # resultData = root


        elif method_msg == "setBuildSettings":
            ObjectId = int(parametrs_msg.find("ObjectID").text)
            objectsSettings = parametrs_msg.find("objectsSettings")
            objects = xmltodict.parse(ET.tostring(objectsSettings))["objectsSettings"]
            for key in objects.keys():
                data = dict(objects[key])
                data["ObjectId"] = ObjectId
                iDB.AR_db.setNewObjectBuildSettings(data)
                print(data)
            result = ET.Element('result')
            result.text = "OK"
            resultData = result


        # elif methodJSON == "getLast":
        #     parametrsMsg = msg["parametrs"]
        #     collectionId = int(parametrsMsg["ObjectID"])
        #     result = iDB.AR_db.getLastOne(iDB.AR_db.getNameOfCollection(collectionId))
        #     resultData = result
        #
        elif method_msg == "getWarning":

            collectionId = int(parametrs_msg.find("ObjectID").text)
            if collectionId == 1:
                result_str = str("Only the temperature sensor works!")
            else:
                result_str = str("Empty")
            result = ET.Element('result')
            result.text = result_str
            resultData = result
        #
        # # elif methodJSON == "getLastData":
        # #     collectionId = int(msg["ObjectID"])
        # #     result = iDB.getLastOne(iDB.getNameOfCollection(collectionId))
        # #     resultData = result
        #
        elif method_msg == "getPublicKey":
            key = RSA.importKey(open('publickey.pem').read())
            key.export_key()
            resultData= str(key.export_key())
            result = ET.Element('result')
            result.text = resultData
            resultData = result


        elif method_msg == "getPrognose":
            collectionId = int(parametrs_msg.find("ObjectID").text)
            result = {"data":float(prognos(collectionId)[0])}
            result = {"data": float(78.58682)}
            # print(result)
            result = json2xml.Json2xml(result).to_xml()  # JSON -> XML string
            # print(result)
            ET.Element("objectsSettings")

            resultData = ET.fromstring(result)  # XML string -> XML

        else:
            resultData = "Wrong Method"
            result = ET.Element('result')
            result.text = resultData
            resultData = result


        return responseJSON(resultData)
    except ImportError:
        # old
        resultData = "Wrong Request"
        # resultData = ""
        result = ET.Element('result')
        result.text = resultData
        return responseJSON(result)


# ответ на запрос
def responseJSON(data):
    """
    Формирует из данных "data" ответ клиенту
    :param data: принимает на вхлд двнные, которые нужно передать тип str с JSON объектом внутри
    :return: сформированное сообщение, готовое к отправке клиенту
    """
    # ------
    # old
    # msg = {}
    # msg["method"] = "response"
    # msg["data"] = data
    # ------
    # new
    msg = ET.Element("message")
    method = ET.SubElement(msg, "method")
    method.text = "response"
    data.tag = "data"
    msg.append(data)
    msg = ET.ElementTree(msg)
    # msg = ET.tostring(msg)

    file_msg = BytesIO()
    msg.write(file_msg, encoding='utf-8', xml_declaration=True)
    return file_msg.getvalue()

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
