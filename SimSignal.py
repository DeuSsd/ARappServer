from ARappServer import DBinterface as iDB
from math import sin, cos
import time

f = open('data.txt', 'w')

power = open('power.txt', "r")



# function of simulate signal
def signal(x):
    y = (10 * (sin(3 * x) * cos(1.4 * x) + cos(x)) + 8 * sin(x) - 9 * cos(2 * x)) + 70
    return y


# simulate signal
x = -20
i = 1
while True:
    power.seek(0)  # возвращаемся в начало документа
    powerStatus = power.read()
    if powerStatus.rstrip() == "True":
        x += 0.01
    if x > 20:
        x = -20
    f.seek(0)  # возвращаем положение курсора в начало файла
    # x = datetime.now().second
    time.sleep(0.5)
    y = signal(x)
    f.write(str(y))
    # print(i,y)

        # i+=1