from rdflib import *
from NN_tools import *
from NN_tools_execute import execute
from IMS_2 import ims
import os

ACCURACY = 0.0005

g = Graph()
file = open("KB.n3", "rb")
result = g.parse(source="KB.n3", format="n3")
file.close()

for subj, pred, obj in g:
    if (subj, pred, obj) not in g:
        raise Exception("N3 с ошибками!")

print("\n\033[36mГраф имеет {} триплетов!\033[36m".format(len(g)))


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
print("\nПуть к нейросетевому хранилищу: ", path_nn)

# Конвертирует словарь параметров в список
def convert_dict_to_ilst(dict_parametrs):
    l = len(dict_parametrs)
    list_parametrs = []
    for i in range(l):
        list_parametrs.append(dict_parametrs[i+1])
    return list_parametrs

def add_new_nn_to_KB(new_name):
    NN = Namespace('file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#')
    g.bind("NN", NN)
    new_name = new_name.split("\\")[-1].split(".")[0]
    new_obj = NN[:-1] + "Predicate_" + new_name
    g.add((new_obj, RDF.type, NN.NN_Model))
    print("\033[36mГраф имеет {} триплетов!".format(len(g)))
    g.add((new_obj, NN.model_name, Literal(new_name)))
    print("\033[36mГраф имеет {} триплетов!".format(len(g)))
    g.add((new_obj, NN.active, Literal(True)))
    print("\033[36mГраф имеет {} триплетов!".format(len(g)))

    file = open("KB.n3", mode="wb")
    file.write(g.serialize(format="n3"))
    file.close()


# Изменение статуса
def change_status(new_name):
    q = g.query(
        '''
        PREFIX NN: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?Name
        WHERE
        {
            ?Name a NN:NN_Model .
            ?Name NN:active true .
        }
           ''')

    for Name_Model in q:
        nn_model_name = item[0]
        # NN = URIRef(":")
        NN = Namespace('file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#')
        g.bind("NN", NN)
        g.set((Name_Model[0], NN.active, Literal(False)))

    add_new_nn_to_KB(new_name)

    # Запись в базу знаний, сохранение
    file = open("KB.n3", mode="wb")
    file.write(g.serialize(format="n3"))
    file.close()

while True:
    # # ////////////////////////////////////////////////////////////////////////////////
    # Выводим список объектов
    q = g.query('''
                PREFIX MyBase: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                SELECT ?Object ?Name
                WHERE
                {
                    ?Object a MyBase:hardware.
                    ?Object MyBase:name ?Name.
                }
    ''')

    hardware_list = {}
    num = 1
    for item,name in q:
        hardware_list[num] = (item.split("#")[-1],str(name))
        num+=1
    num-=1
    print(hardware_list)

    file = open("KB.n3", mode="wb")
    file.write(g.serialize(format="n3"))
    file.close()
    # Выбор объекта
    print("\033[95mКоличество подключенного оборудования - ",num, ":")
    for i in range(num):
        print("["+str(i+1)+"] - "+hardware_list[i+1][-1])
    number_of_picked_system = int(input("Выберите для наблюдения систему под номером: \033[36m"))
    picked_system = hardware_list[number_of_picked_system][0]
    # ////////////////////////////////////////////////////////////////////////////////

    q = g.query(
        '''
        PREFIX MyBase: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?param_formula
        WHERE
        {
            MyBase:'''+picked_system+''' MyBase:formula ?param_formula .
        }
    ''')

    formula_item = ""
    for item in q:
        formula_item = item[0].split("#")[-1]

    # print(formula_item)
    q = g.query('''
            PREFIX FORMULA: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/formulas/#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?formula_name
            WHERE
            {
                FORMULA:''' + formula_item + ''' FORMULA:formula_name ?formula_name .
            }
    ''')
    formula_name = ""
    for item in q:
        formula_name = item[0]
    print("Используемая формула - ", formula_name)
    # Получаем количество параметров функции
    q = g.query(
        '''
        PREFIX FORMULA: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/formulas/#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?num
        WHERE
        {
            FORMULA:''' + formula_item + ''' FORMULA:numparam ?num .
        }
    ''')

    number_of_parametrs = 0
    for i in q:
        number_of_parametrs = i[0]
        # print(i[0])

    # Получаем параметры функции
    parametrs_of_function = {}
    for i in range(int(number_of_parametrs) + 1):
        q = g.query('''
                PREFIX FORMULA: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/formulas/#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
                SELECT ?param
                WHERE
                {
                    FORMULA:''' + formula_item + ''' rdf:_''' + str(i) + ''' ?param .
                }
        ''')
        for item in q:
            parametrs_of_function[i] = str(item[0])
    # print(parametrs_of_function)

    # Получаем название выхода функции
    q = g.query('''
                PREFIX FORMULA: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/formulas/#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
                SELECT ?param
                WHERE
                {
                    FORMULA:''' + formula_item + ''' FORMULA:exit_param ?param .
                }
    ''')
    exit_parametr = ""
    for item in q:
        exit_parametr = item[0].split("#")[-1]
    # print(exit_parametr)

    input_names = convert_dict_to_ilst(parametrs_of_function)  # список входных параметров
    output_names = [exit_parametr]  # список выходных параметров
    print("Входные и выходные параметры формулы - ",input_names,output_names)
    # ////////////////////////////////////////////////////////////////////////////////

    ims(
        formula_name,
        'data.csv',
        input_names,
        output_names
    )




    # ////////////////////////////////////////////////////////////////////////////////
    # узнаём базовые параметры для обучения
    q = g.query('''
            PREFIX NN: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?num_n ?num_l
            WHERE
            {
                NN:base_parametrs_nn_model NN:number_of_neurons ?num_n .
                NN:base_parametrs_nn_model NN:number_of_layer ?num_l .
            }
    ''')
    number_of_neurons = 0
    number_of_layer = 0

    for item in q:
        number_of_neurons = int(item[0])
        number_of_layer = int(item[1])

    print("\033[95mКоличество внутренних слоёв - {}\n"
          "Количество нейронов в каждом внутреннем слое - {}\033[36m".format(number_of_layer,number_of_neurons ))

# ////////////////////////////////////////////////////////////////////////////////

# while True:
    # узнаём есть ли нейросетевые модели в базе и если есть забираем последнюю
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

    # затестить
    # def objects(self, subject=None, predicate=None):
    #     """A generator of objects with the given subject and predicate"""
    #     formula s, p, o in self.triples((subject, predicate, None)):
    #         yield o

    result = False
    base_nn_model_name = ""
    nn_model_name = ""

    # Удаление лишних знаний
    if len(q) != 0 and len(os.listdir(path_nn)) == 0:
        print("\033[36mГраф имеет {} триплетов!\n"
        "Удаление лишних знаний".format(len(g)))
        q = g.query(
            '''
            PREFIX NN: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            
            SELECT ?instance ?status
            
            WHERE
            {
                ?instance a NN:NN_Model;
                    NN:active ?status .
            }
            ''')

        for name, status in q:
            g.remove((name, None, None))
            print("\033[36mГраф имеет {} триплетов!".format(len(g)))

    # ---
    # Запрос готовых нейросетевых моделей
    q = g.query(
        '''
        PREFIX NN_tools: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/NN_tools/#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?instance ?action ?name
        WHERE
        {
            ?instance a NN_tools:algorithm .
            ?instance NN_tools:action ?action .
            ?instance NN_tools:name ?name .
        }
    ''')

    NN_tools = {}
    for _, action, name in q:
        NN_tools[name] = action


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


    if len(q) == 0:

        print("\033[95mнейросетевой модели нет\033[36m")

        q = g.query(
            '''
            PREFIX NN: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/NN/#>
            SELECT ?model_name
            WHERE
            {
                NN:NN_Model NN:base_model_name ?model_name.
            }
            '''
        )
        for item in q:
            # print(item)
            # name = item[0].split("#")[1]
            base_nn_model_name = item[0]
            # print(name)
        base_nn_model_name += "1"
        # print(base_nn_model_name)
        nn_model_name = os.path.join(path_nn, base_nn_model_name + ".h5")
        # print(nn_model_name)
        # обучение нейросети
        accuracy = 0
        while accuracy < ACCURACY:

            # learn_nn.learn_nn(
            #     nn_model_name,
            #     input_names,
            #     output_names,
            #     "data.csv",
            #     number_of_neurons,
            #     number_of_layer
            # )
            execute("learn_nn", [
                nn_model_name,
                input_names,
                output_names,
                ["data.csv"],
                number_of_neurons,
                number_of_layer
            ])

            accuracy = execute(
                "test_nn",[
                [nn_model_name],
                input_names,
                output_names,
                ["data.csv"]
            ])
            # accuracy = test_nn(
            #     nn_model_name,
            #     input_names,
            #     output_names,
            #     "data.csv"
            # )

            print("\033[95mКоличество внутренних слоёв - {}\n"
                  "Количество нейронов в каждом внутреннем слое - {}\n"
                  "Текущая точность прогностической модели - {}\033[36m".format(number_of_layer, number_of_neurons,
                                                                                accuracy))

            if number_of_neurons < 0:
                number_of_neurons+=1
            elif number_of_layer < 0:
                number_of_layer += 1
            else:
                break

        print("\033[95mПрогностическая модель - {}\033[36m".format(base_nn_model_name))
        # add_new_nn_to_KB(nn_model_name)
        change_status(nn_model_name)
    else:
        print("\033[95mнейросетевая модель есть\033[36m")
        # print(len(q))
        for item in q:
            nn_model_name = item[0].split("#")[1]
            # print(nn_model_name)

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
            print("\033[95mПрогностическая модель - {}\033[36m".format(nn_model_name))

        full_path_nn_model = os.path.join(path_nn, nn_model_name + ".h5")
        # print(full_path_nn_model)


        # accuracy = test_nn(
        #             full_path_nn_model,
        #             input_names,
        #             output_names,
        #             "data.csv"
        #         )
        accuracy = execute(
            "test_nn",[
                [full_path_nn_model],
                input_names,
                output_names,
                [ "data.csv"]
            ])
        #         #проверка нейросети

        print("\033[95mКолличество внутренних слоёв - {}\n"
              "Количество нейронов в каждом внутреннем слое - {}\n"
              "Текущая точность прогностической модели - {}\033[36m".format(number_of_layer, number_of_neurons,accuracy))

        if accuracy < ACCURACY:
            # relearn_nn.relearn_nn(
            #     full_path_nn_model,
            #     input_names,
            #     output_names,
            #     "data.csv"
            # )
            execute(
                "relearn_nn", [
                    [full_path_nn_model],
                    input_names,
                    output_names,
                    ["data.csv"]
            ])
            # accuracy = test_nn(
            #     full_path_nn_model,
            #     input_names,
            #     output_names,
            #     "data.csv"
            # )  # проверка нейросети
            accuracy = execute(
                "test_nn", [
                    [full_path_nn_model],
                    input_names,
                    output_names,
                    ["data.csv"]
                ])

            print("\033[95mКолличество внутренних слоёв - {}\n"
                  "Колличество нейронов в каждом внутреннем слое - {}\n"
                  "Текущая точность прогностической модели - {}\033[36m".format(number_of_layer, number_of_neurons,
                                                                                accuracy))
            if accuracy < ACCURACY:
                name,i_num = nn_model_name.split("_")
                name += "_{}".format(int(i_num)+1)
                nn_model_name = os.path.join(path_nn, name + ".h5")
                # обучение нейросети
                accuracy = 0
                while accuracy < ACCURACY:

                    # learn_nn.learn_nn(
                    #     nn_model_name,
                    #     input_names,
                    #     output_names,
                    #     "data.csv",
                    #     number_of_neurons,
                    #     number_of_layer
                    # )
                    execute("learn_nn", [
                        [nn_model_name],
                        input_names,
                        output_names,
                        ["data.csv"],
                        number_of_neurons,
                        number_of_layer
                    ])
                    #
                    # accuracy = test_nn(
                    #     nn_model_name,
                    #     input_names,
                    #     output_names,
                    #     "data.csv"
                    # )
                    accuracy = execute(
                        "test_nn", [
                            [nn_model_name],
                            input_names,
                            output_names,
                            ["data.csv"]
                        ])
                    print("\033[95mКоличество внутренних слоёв - {}\n"
                          "Количество нейронов в каждом внутреннем слое - {}\n"
                          "Текущая точность прогностической модели - {}\033[36m".format(number_of_layer,
                                                                                        number_of_neurons, accuracy))

                    if number_of_neurons < 25:
                        number_of_neurons += 1
                    elif number_of_layer < 6:
                        number_of_layer += 1
                    else:
                        break
                # add_new_nn_to_KB(nn_model_name)
                change_status(nn_model_name)
                print("\033[95mНовая прогностическая модель - {}\033[36m".format(name))
            else:
                # print(1)
                change_status(nn_model_name)


    # q = g.query('''
    #             PREFIX MyBase: <file:///U:/7%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80/pythonProject/MyBase/#>
    #             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #
    #             SELECT ?p ?s
    #             WHERE
    #             {
    #                 MyBase:''' + picked_system + ''' ?p ?s.
    #             }
    # ''')
    #
    # for p, s in q:
    #     print(p.split("#")[-1], s)

    # if input():
    #     break

    # print("\033[36mГраф имеет {} триплетов!".format(len(g)))
    # # print("\033[35m {} !".format([i formula i in g.namespaces()]))
    # break

# ################################





