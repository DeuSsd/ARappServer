from rdflib import *
from ARappServer.NN_tools.predict_nn import predict_nn,forecast_nn

import os

def prognos(
        CollectionId,
        num_future = 100,
        window = 10
):
    g = Graph()
    file = open("KB.n3", "rb")
    result = g.parse(source="KB.n3", format="n3")
    file.close()

    # извлекаем путь к нейросетевым моделям
    path_nn = ''
    q = g.query(
        '''
        PREFIX NN: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?path_model
    
        WHERE
        {
            NN:NN_Model NN:path ?path_model .
        }
        ''')


    for item in q:
        path_nn = item[0]
    # print("\nПуть к нейросетевому хранилищу: ", path_nn)

    # Запрос готовых нейросетевых моделей
    q = g.query(
        '''
        PREFIX NN: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?instance
        WHERE
        {
            ?instance a NN:NN_Model .
            ?instance NN:active true .
        }
    ''')

    nn_model_name = ""

    if q!=0:
        for item in q:
            nn_model_name = item[0].split("#")[-1]

        q = g.query(
            '''
            PREFIX NN: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
            SELECT ?Name
            WHERE
            {
                NN:''' + nn_model_name + ''' NN:model_name ?Name .
                NN:''' + nn_model_name + ''' NN:active true  .
            }
            ''')

        for item in q:
            nn_model_name = item[0]
            # print("\033[95mПрогностическая модель - {}\033[36m".format(nn_model_name))

        full_path_nn_model = os.path.join(path_nn, nn_model_name + ".h5")

        predict = forecast_nn([full_path_nn_model],CollectionId,num_future=num_future,window=window)

        return predict.reshape((predict.shape[-2]))
    else:

        # means nothing
        return -100


if __name__ == '__main__':
    print(prognos(1, num_future = 200,window = 20))
