import keras as k
from sklearn.utils import shuffle
import pandas as pd
import numpy as np

# переобучение готовой нейросети
def relearn_nn(nn_name,  # имя нейросетевой модели
             input_names,  # список входных параметров
             output_names,  # список выходных параметров
             dataset_name,  # название датасета .csv
             ):
    nn_name = nn_name[0]
    dataset_name = dataset_name[0]
    # print(nn_name)
    model = k.models.load_model(nn_name)

    epochs = 10

    data_frame = pd.read_csv(dataset_name)

    columns = data_frame.shape[0]
    data_frame = shuffle(data_frame)
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

    # early_stopping_patience = 10
    # Add early stopping
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

    # predict = model.predict(test_x)
    #
    # print()
    # eps = sum / len(predict)
    # print("\033[36m", sum, eps)
    # print("\033[35mEvaluate")
    # result = model.evaluate(test_x, test_y)
    # dict(zip(model.metrics_names, result))
