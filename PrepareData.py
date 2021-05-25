from ARappServer.DBinterface import AR_db
import pandas as pd
import numpy as np

def _prepareData(objectID,limit = 10):
    '''
    Извлечение данных и их подготовка для подачи на вход нейросети

    :param objectID: id физического объекта
    :param limit: колическтво данных, извлекаемых из БД
    :return: извлечённые данные типа DataFrame
    '''

    #TODO по id извлечь labels
    labels = ["temp1"]
    data = AR_db.getManyByID(objectID,limit=limit)

    preparedData = []
    for item in data:
        temp = []
        for label in labels:
            temp.append(item[label])
        preparedData.append(temp)

    df = pd.DataFrame(preparedData,columns=labels)
    return df

def _reshapeData(dataFrame,window = 10):
    '''
    Представление данных для подачи на вход нейросети LSTM

    :param dataFrame: входной датафрейм данных
    :param window: размер окна, по умолчанию равен 10
    :return: два массива типа NumPy: массив с историческими данными
    и данными, необходимые для соотнесения обучения, т.е подаваемых на выход LSTM
     data_past - input
     data_next - output  - предсказанные данные
    '''
    data_past = []
    data_next = []

    for i in range(window, len(dataFrame)):
        data_past.append(dataFrame.iloc[i - window:i])
        data_next.append(dataFrame.iloc[i])

    return np.array(data_past), np.array(data_next)



def prepareDataForTrain(ObjectID,quantity,window = 10):
    '''
    Подготовка данных для обучения нейронной сети LSTM
    :param ObjectID:  id физического объекта
    :param quantity:  количество извлекаемых данных
    :param window: размер окна обучения
    :return: два массива типа NumPy: массив с историческими данными
    и данными, необходимые для соотнесения обучения, т.е подаваемых на выход LSTM
     data_past - input
     data_next - output  - предсказанные данные
    '''
    dataFrame = _prepareData(ObjectID,quantity)
    data_past,data_next = _reshapeData(dataFrame, window=window)
    return data_past,data_next

def prepareDataForPredict(ObjectID,window = 10):
    '''
    Подготовка данных для предсказания
    нейронная сеть - LSTM
    :param ObjectID: id физического объекта
    :param window: размер окна обучения и
    по совместительству количество извлекаемых данных
    :return: массива типа NumPy с последними историческими данными
    '''
    dataFrame = _prepareData(ObjectID, window)
    data = np.array([dataFrame])
    return data

if __name__ == "__main__":
    x = prepareDataForPredict(1)
    print(x.shape)