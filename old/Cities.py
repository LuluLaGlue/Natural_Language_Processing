import spacy
import random
import pandas as pd
import geonamescache
from geotext import GeoText

gc = geonamescache.GeonamesCache()

nlp = spacy.load('fr_core_news_lg')

queries = pd.read_csv('./data/txt/query.txt', sep=";")
train_station = pd.read_csv('./data/csv/list_train_stations.csv', sep=";")
final_queries = []
res = []

train_station.pop("id")

print(train_station.head())

for station in train_station["station"]:
    index_1 = random.randrange(len(queries["query"]) - 1)
    index_2 = random.randrange(len(train_station["station"]) - 1)
    final_queries.append(queries["query"][index_1].replace(
        "$1", " ".join(str(station).split("-"))).replace(
            "$2", " ".join(str(train_station["station"][index_2]).split("-"))))

print(final_queries[:10])
print("Number of Train Station: ", len(final_queries))

list_cities = gc.get_cities()
all_cities = []
cities = []

for city in list_cities:
    all_cities.append(list_cities[city]['name'].lower())
    for alternate in list_cities[city]['alternatenames']:
        dash = alternate.split('-')
        dash = ' '.join(dash).lower()
        all_cities.append(dash)

list_cities = None

for file in final_queries:
    doc = nlp(file)

    for ent in doc.ents:
        location = ent.text.split('-')
        location = " ".join(location).lower()
        if location in all_cities:
            cities.append(location)
        else:
            string = GeoText(location)
            if len(string.cities) != 0:
                cities.append(location)

print(cities)
print("Found {} cities".format(len(cities)))