from server import DBinterface as iDB
import datetime
from datetime import timezone
import ast

def loadMessage(msg):
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
        return responseJSON(resultData)
    except:
        resultData = "Wrong Request"
        return responseJSON(resultData)

# ответ на запрос
def responseJSON(data):
    msg = {}
    msg["method"] = "response"
    msg["data"] = data
    return msg

#/////////////////test/////////////////
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
