from ARappServer import DBinterface as iDB
import csv
import datetime as dt

def ims():
    data = iDB.AR_db.getMany(iDB.AR_db.getNameOfCollection(1))
    data_csv = []
    data_csv.append(["Date", "Temperature"])
    for item in data:
        time = dt.datetime.strptime(item["Date"], "%Y-%m-%d %H:%M:%S.%f%z")
        data_csv.append([time.timestamp(), float(item["Temperature"])])

    csv_file = open("data.csv", 'w')

    with csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data_csv)
        print("\033[91mДанные подготовлены\033[36m")
        csv_file.close()

if __name__=="__main__":
    ims()

