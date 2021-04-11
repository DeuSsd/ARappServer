import keras
import matplotlib.pyplot as plt
from FunExec import execute

# print(execute(formula_name, [2, 2, 6]))

import pandas as pd
import numpy as np
from sklearn.utils import shuffle

# проверка существующей нейросети
def test_nn(
        nn_name,  # имя нейросетевой модели
        input_names,  # список входных параметров
        output_names,  # список выходных параметров
        # funName,  # имя тестовой функции
        dataset_name,  # название датасета .csv
):
    # print(nn_name)
    nn_name = nn_name[0]
    dataset_name = dataset_name[0]
    model = keras.models.load_model(nn_name)


    data_frame = pd.read_csv(dataset_name)

    columns = data_frame.shape[0]

    # перемешивание данных
    data_frame = shuffle(data_frame)

    # data_frame=data_frame.shuffle(buffer_size=1024).batch(64)

    # input_names = ["A","k","w","x"]
    # input_names = ["k","w","x"]
    # input_names = ["x"]
    # output_names = ["f"]
    # input_names = ["a", "b"]
    # output_names = ["c"]

    def dataframe_to_dict(df):
        result = dict()
        max = df.max()

        for column in df.columns:
            values = df[column] / max[column]

            result[column] = values
        return result

    # print(input_names, output_names)

    def make_supervised(df):
        raw_in_data = df[input_names]
        raw_out_data = df[output_names]
        return {"in": dataframe_to_dict(raw_in_data),
                "out": dataframe_to_dict(raw_out_data)}

    def encode(data):
        vectors = []
        for data_name, data_values in data.items():
            vectors.append(list(data_values))

        formatted = []

        for vector_raw in list(zip(*vectors)):
            formatted.append(list(vector_raw))

        return formatted

    supervised = make_supervised(data_frame)

    in_data = np.array(encode(supervised["in"]))
    out_data = np.array(encode(supervised["out"]))

    # print(round(columns * 0.8))

    test_x = in_data[round(columns * 0.8):]
    test_y = out_data[round(columns * 0.8):]
    result = model.evaluate(test_x,test_y)
    return result[1]

    # rezult_data = {}
    # model = keras.models.load_model(nn_name)
    # # data_x = []
    # # data_n = []
    # # data_f = []
    #
    # # A = random.randint(-10, 10)
    # # k = random.randint(-10, 10)
    # # w = random.randint(-10, 10)
    # # A = k = w = 1
    # # i = 10
    # #
    # # x = -i
    #
    # while x < i:
    #     # f = k * x + w
    #     # f = A * sin(k * x + w)
    #     f = k * x + w
    #     predict = model.predict([[x]])
    #     n1 = predict[0][0]
    #     data_x.append(x)
    #     data_f.append(f)
    #     data_n.append(n1)
    #     x += 0.5
    #
    # plt.plot(data_x, data_f, color='red')
    # plt.plot(data_x, data_n, color='blue')
    # plt.title("math.sin()")
    # plt.xlabel("X")
    # plt.ylabel("Y")
    # plt.show()
    # return False if random.randint(-2, 2) >= 0 else True
    # # return True
    # # return False


if __name__ == "__main__":
    test_nn(
        "U:\\7 семестр\pythonProject\Models\Model_1.h5",
        ['x', 'b', 'c'],
        ['y'],
        "linear",
        "data.csv"
    )
    # # model = k.models.load_model("Models\Model_1.h5")
    # #
    # from math import sin
    #
    # data_x = []
    # data_n = []
    # data_f = []
    #
    # A = random.randint(-10, 10)
    # k = random.randint(-10, 10)
    # w = random.randint(-10, 10)
    # A = k = w = 1
    # i = 10
    #
    # x = -i
    #
    # while x < i:
    #     # f = k * x + w
    #     # f = A * sin(k * x + w)
    #     f = k * x + w
    #     predict = model.predict([[x]])
    #     n1 = predict[0][0]
    #     data_x.append(x)
    #     data_f.append(f)
    #     data_n.append(n1)
    #     x += 0.5
    #
    # plt.plot(data_x, data_f, color='red')
    # plt.plot(data_x, data_n, color='blue')
    # plt.title("math.sin()")
    # plt.xlabel("X")
    # plt.ylabel("Y")
    # plt.show()
