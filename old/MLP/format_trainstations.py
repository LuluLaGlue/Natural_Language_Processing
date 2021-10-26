import pandas as pd

df = pd.read_csv("./data/csv/timetables.csv", sep="\t")
train_stations_formated = []
train_stations_brut = []

for stations in df["trajet"]:
    for station in stations.split(' - '):
        train_stations_brut.append(station)
        station = station.replace('-/-', '-sur-')
        if len(station.split(' de ')) > 1:
            train_stations_formated.append(station.split(' de ')[1].lower())
        else:
            train_stations_formated.append(station.lower())

train_stations_formated = list(set(train_stations_formated))
train_stations_brut = list(set(train_stations_brut))

train_stations_formated = pd.DataFrame(train_stations_formated)
train_stations_brut = pd.DataFrame(train_stations_brut)

train_stations_formated.to_csv("./data/csv/list_train_stations.csv", sep=";")
train_stations_brut.to_csv("./data/csv/list_train_stations_brut.csv", sep=";")