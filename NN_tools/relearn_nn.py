from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
from keras import callbacks
from keras.models import load_model

from ARappServer.PrepareData import prepareDataForTrain

'''
метод переобучения нейронной сети
'''

# переобучение готовой нейросети
def relearn_nn(nn_name,  # имя нейросетевой модели
        objectID,
        trainSize=2000,
        epochs = 200,
        window = 25,
        num_blocks_LSTM = 10,
        ):
    nn_name = nn_name[0]

    model = load_model(nn_name)

    # dataFrame = pd.DataFrame(pd.read_csv(dataset_name)["X"],columns=["X"])
    # print(dataFrame,dataFrame.shape)

    nn_name = nn_name[0]
    # Set window of past points for LSTM model

    # извлекаем данные для обучения
    xin, next_X = prepareDataForTrain(objectID, trainSize, window=window)

    callback = callbacks.EarlyStopping(
        monitor='loss', patience=10, restore_best_weights=True, min_delta=0.01
    )
    # Fit LSTM model
    model.fit(
        xin,
        next_X,
        epochs=epochs,
        batch_size=num_blocks_LSTM,
        verbose=1,
        validation_split=0.2,   #add
        callbacks=callback,
        shuffle=True
    )

    model.save(nn_name)
    #сохранение полученной нейросетевой модели

if __name__ == "__main__":
    relearn_nn(["test.h5"],
               1,
               1,
               1,
                trainSize=2500,
                epochs=100,
                window=20
               )