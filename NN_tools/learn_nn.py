from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
from keras import callbacks

from ARappServer.PrepareData import prepareDataForTrain

'''
Метод обучения нейронной сети
'''

def learn_nn(nn_name,  # имя нейросетевой модели
             number_of_neurons,  # количество нейронов в LSTM слое
             number_of_layer  # количество LSTM слоёв в нейросетевой модели
             ):

    # dataFrame = pd.DataFrame(pd.read_csv(dataset_name)["X"],columns=["X"])
    # print(dataFrame,dataFrame.shape)

    nn_name = nn_name[0]
    epochs = 200
    window = 10         # Set window of past points for LSTM model

    # извлекаем данные для обучения
    xin,next_X = prepareDataForTrain(1,5000)
    outputNum = next_X.shape[-1]

    # Initialize LSTM model
    model = Sequential()
    num_blocks_LSTM = 100
    model.add(LSTM(units=num_blocks_LSTM, return_sequences=True, input_shape=(xin.shape[-2:])))
    model.add(Dropout(0.2))
    model.add(LSTM(units=num_blocks_LSTM))
    model.add(Dropout(0.2))
    model.add(Dense(units=outputNum))
    model.compile(
        optimizer='adam',
        loss='mean_squared_error',
        metrics = 'mse'
    )

    callback = callbacks.EarlyStopping(
        monitor='loss', patience=20, restore_best_weights=True, min_delta=0.01
    )

    # Fit LSTM model
    history = model.fit(
        xin,
        next_X,
        epochs=200,
        batch_size=num_blocks_LSTM,
        verbose=0,
        callbacks=callback
    )

    model.save(nn_name)

if __name__ == "__main__":
    learn_nn(["test.h5"],
        1,1
    )