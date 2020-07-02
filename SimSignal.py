from math import sin, cos
from datetime import datetime
import time

f = open('data.txt', 'w')


# function of simulate signal
def signal(x):
    y = (10 * (sin(3 * x) * cos(1.4 * x) + cos(x)) + 8 * sin(x) - 9 * cos(2 * x)) + 70
    return y


# simulate signal
x = -20
i = 1
while True:
    if x > 20:
        x = -20
    f.seek(0)  # возвращаем положение курсора в начало файла
    # x = datetime.now().second
    # time.sleep(1)
    y = signal(x)
    f.write(str(y))
    # print(i,y)
    x += 0.02
    # i+=1
