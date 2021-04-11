from random import seed
import keras as k
from sklearn.utils import shuffle
import pandas as pd
import numpy as np

'''
Метод обучения нейронной сети
    
'''


def learn_nn(nn_name,  # имя нейросетевой модели
             input_names,  # список входных параметров
             output_names,  # список выходных параметров
             dataset_name,  # название датасета .csv
             number_of_neurons,  # количество нейронов в слое
             number_of_layer  # количество слоёв в нейросетевой модели
             ):
    nn_name = nn_name[0]
    dataset_name = dataset_name[0]
    # print(nn_name)
    # activation="relu"
    # activation="tanh"
    activation = "relu"

    epochs = 10

    # seed()
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

    # print(input_names,output_names)
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

    train_x = in_data[:round(columns * 0.8)]
    train_y = out_data[:round(columns * 0.8)]

    test_x = in_data[round(columns * 0.8):]
    test_y = out_data[round(columns * 0.8):]
    # print("type",number_of_layer,type(number_of_layer))
    print("\033[33m==========",
          len(input_names),
          (str(number_of_neurons) + ",") * number_of_layer,
          len(output_names),
          "==========\033[34m")

    # Начало сборки модели
    model = k.Sequential()
    initializer = k.initializers.TruncatedNormal(seed=seed())  # задаём сид, для случайных весов

    # входной слой
    model.add(k.layers.Dense(units=len(input_names),
                             input_dim=len(input_names),
                             # kernel_initializer = initializer,
                             # activation = None,
                             # activation="relu",
                             # activation="tanh",
                             ))
    # скрытые слои
    for i in range(number_of_layer):
        model.add(k.layers.Dense(units=number_of_neurons,
                                 kernel_initializer=initializer,
                                 activation=activation))
    # выходной слой
    model.add(k.layers.Dense(units=len(output_names),
                             kernel_initializer=initializer,
                             activation = None,
                             # activation='linear',
                             ))

    opt = k.optimizers.Adam(learning_rate=0.01)

    model.compile(
        loss='mse',
        # optimizer="sgd",
        # optimizer="adam",
        optimizer=opt,
        metrics="accuracy",
    )

    # early_stopping_patience = 10
    # # Add early stopping
    # early_stopping = k.callbacks.EarlyStopping(
    #     monitor="val_loss", patience=early_stopping_patience, restore_best_weights=True
    # )

    # callback = k.callbacks.EarlyStopping(
    #     monitor='loss', patience=3, restore_best_weights=True, min_delta= 0.01
    # )
    #

    fit_results = model.fit(
        x=train_x,
        y=train_y,
        epochs=epochs,
        validation_split=0.2,
        # callbacks=[early_stopping
        #            ],
        batch_size=32,
    )


    model.save(nn_name)#сохранение полученной нейросетевой модели

    # plt.title("train/validation")
    # plt.plot(fit_results.history["accuracy"],label = "Train")
    # plt.plot(fit_results.history["val_accuracy"], label = "Validation")
    # plt.legend()
    # plt.show()
    #
    # predict = model.predict(test_x)
    #
    # sum = 0
    # for item in range(len(predict)):
    #     el1 = abs(predict[item][0])
    #     el2 = abs((test_x[item][-1]))
    #     delta = abs(el1 - el2)
    #     sum += delta
    #     # print(delta)
    #
    # print()
    # eps = sum / len(predict)
    # print("\033[36m", sum, eps)
    # print("\033[35mEvaluate")
    # result = model.evaluate(test_x, test_y)
    # dict(zip(model.metrics_names, result))

# plt.title("loss/validation")
# plt.plot(fit_results.history["loss"],label = "Train")
# plt.plot(fit_results.history["val_loss"], label = "Validation")
# plt.legend()
# plt.show()
