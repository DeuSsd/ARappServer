# Python program showing
# Graphical representation of
# sin() function
from math import sin
import matplotlib.pyplot as plt


# in_data = []
# out_data = []
#
# data = []
# data.append(["A","k","w","x","f"])

# def fun(parametrs):
#     x = -10
#     while x<10:
#         in_data.append(x)
#         f = k*x+w
#         # f = A*sin(k*x+w)
#         # f = x*x*A+ x*k +w
#         out_data.append(f)
#         data.append([A,k,w,x,f])
#         x+=1
#
# # i = 10
# while i > 0:
#     fun(1,0.5,0)
#     i-= 1

# param = [[random.randint(-10,10),random.randint(-10,10),random.randint(-10, 10)] formula i in range(100)]
# param = [[1,1,1] for i in range(100)]
# for item in param:
#     fun(*item)


#
# plt.plot(in_data, out_data, color='red')
# plt.title("math.sin()")
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.show()


from FunExec import execute
import csv
import random

def ims(
        formula_name,
        data_csv,
        input_names,
        output_names
):
    # print(input_names,output_names)
    names = input_names+output_names

    data = []
    data.append(names)

    parametrs = [[round(random.random()*100-50,2) for i in range(len(input_names))] for i in range(10000)]
    for item in parametrs:
        f = execute(formula_name, item)
        # print(item+[f])
        data.append(item+[f])

    csv_file = open(data_csv, 'w')

    with csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)
        print("\033[91mДанные подготовлены\033[36m")
    return None
    csv_file.close()