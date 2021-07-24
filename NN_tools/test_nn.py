from ARappServer.PrepareData import prepareDataForPredict,prepareDataForTrain,prepareDataForTest
from ARappServer.NN_tools.predict_nn import forecast_nn,predict_nn,predict_nn_test
import numpy as np

# проверка существующей нейросети
def test_nn(
        nn_name,  # имя нейросетевой модели
        objectID,
        sizeDataSet = 300,
        window = 10
):
    nn_name = nn_name[0]
    if sizeDataSet <= window:
        sizeDataSet = 2*window

    # _,pastDataSet = prepareDataForTrain(objectID,sizeDataSet,window=window)
    df,pastDataSet = prepareDataForTest(objectID,sizeDataSet,window=window)
    # predictDataSet = forecast_nn([nn_name],objectID,num_future=sizeDataSet,window=window)
    predictDataSet = predict_nn_test([nn_name],objectID,df,num_future=sizeDataSet-window,window=window)

    # error = np.sum(abs(predictDataSet - pastDataSet)) / len(pastDataSet)
    # error = np.sum(abs((predictDataSet - pastDataSet)/pastDataSet)) / len(pastDataSet)
    error = np.sum(abs(predictDataSet - pastDataSet)/pastDataSet)/ sizeDataSet

    # error_ms = np.sum(pastDataSet) / len(pastDataSet)
    # error = error_meas/error_ms
    # print("error {}".format(error))
    return abs(error)

if __name__ == "__main__":
    test_nn(
        ["test.h5"],
        1,
        sizeDataSet=3000,
        window=20
    )