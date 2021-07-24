from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
from keras import callbacks

from ARappServer.PrepareData import prepareDataForTrain

'''
Метод обучения нейронной сети
'''

def learn_nn(nn_name,  # имя нейросетевой модели
        objectID,
        trainSize=2000,
        epochs = 200,
        window = 25,
        num_blocks_LSTM = 10,
        dropout = 0.20
        ):

    # dataFrame = pd.DataFrame(pd.read_csv(dataset_name)["X"],columns=["X"])
    # print(dataFrame,dataFrame.shape)

    nn_name = nn_name[0]
    # Set window of past points for LSTM model

    # извлекаем данные для обучения
    xin,next_X = prepareDataForTrain(objectID,trainSize,window=window)
    outputNum = next_X.shape[-1]

    # Initialize LSTM model
    model = Sequential()
    model.add(LSTM(units=num_blocks_LSTM,
                   return_sequences=True,
                   input_shape=(xin.shape[-2:]
                   )))
    model.add(LSTM(units=num_blocks_LSTM,
                   return_sequences=False
                   ))
    model.add(Dropout(dropout))
    model.add(Dense(units=outputNum))
    model.compile(
        optimizer='adam',
        loss='mean_squared_error',
        metrics = 'mse'
    )

    callback = callbacks.EarlyStopping(
        monitor='loss', patience= 10, restore_best_weights=True, min_delta=0.01
    )
    # Fit LSTM model
    model.fit(
        xin,
        next_X,
        epochs=epochs,
        batch_size=num_blocks_LSTM,
        verbose=1,
        callbacks=callback,
        validation_split=0.2,
        shuffle=True
    )
    model.save(nn_name)



if __name__ == "__main__":
    learn_nn(["test.h5"],
             1,
             trainSize=2000,
             epochs=20,
             window=20,
             num_blocks_LSTM=50
    )