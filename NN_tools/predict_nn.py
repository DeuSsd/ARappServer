from keras.models import load_model
import pandas as pd
from ARappServer.PrepareData import prepareDataForPredict,prepareDataForTrain
import numpy as np

ObjectID = 1
labels = ["temp1"]

def predict_nn(
        nn_name , # имя нейросетевой модели
        ObjectID,
        num_future,
        window = 10
):

    nn_name = nn_name[0]
    pastData = prepareDataForPredict(ObjectID,window=window)
    dataFrame = pd.DataFrame(pastData[0], columns = labels)
    lastIndex = dataFrame.iloc[-1:].index[0]
    model = load_model(nn_name)

    for i in range(num_future - 1):
        futureData = model.predict(pastData)
        lastIndex += 1
        # print(pastData)
        pastData[0][:-1] = pastData[0][1:]
        pastData[-1][-1] = futureData
        df = pd.DataFrame(pastData[0], columns=labels, index=[lastIndex for i in range(window)]).iloc[-1:]
        dataFrame = dataFrame.append(df)
    # print(dataFrame)
    # for i in range(num_future - 1):
    df, xy = prepareDataForTrain(ObjectID,num_future,window=window)
    df = model.predict(df)
    import matplotlib.pyplot as plt
    # print(dataFrame)
    plt.plot(df)
    plt.plot(xy)
    plt.show()
    return dataFrame



def forecast_nn(
        nn_name , # имя нейросетевой модели
        ObjectID,
        num_future,
        window = 10
):

    nn_name = nn_name[0]
    model = load_model(nn_name)
    df, xy = prepareDataForTrain(ObjectID, num_future, window=window)
    df = model.predict(df)
    return df

if __name__ == "__main__":
    # forecast()
    dataFrame = predict_nn(
            ["test.h5"],
        1,
        300,
        15
    )
    print(dataFrame)
    import matplotlib.pyplot as plt
    plt.plot(dataFrame)
    plt.show()
