from ARappServer.PrepareData import prepareDataForPredict,prepareDataForTrain
from ARappServer.NN_tools.predict_nn import forecast_nn,predict_nn
import numpy as np

# проверка существующей нейросети
def test_nn(
        nn_name,  # имя нейросетевой модели
        objectID,
        sizeDataSet = 300,
        window = 10
):
    if sizeDataSet <= window:
        sizeDataSet = 2*window
    _,pastDataSet = prepareDataForTrain(objectID,sizeDataSet,window=window)
    predictDataSet = forecast_nn(["test.h5"],objectID,num_future=sizeDataSet,window=window)

    # error = np.sum(abs(predictDataSet - pastDataSet)) / len(pastDataSet)
    error = np.sum(abs(predictDataSet - pastDataSet)/pastDataSet) / len(pastDataSet)
    print("error {}".format(error))
    return error

if __name__ == "__main__":
    test_nn(
        ["test.h5"],
        1,
        sizeDataSet=100,
        window=20
    )