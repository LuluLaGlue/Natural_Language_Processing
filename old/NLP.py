from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import pandas as pd
import spacy
import nltk
import random


class NLP:
    def __init__(self, lang="fr"):
        self.all_cities = []
        self.__list_all_cities()
        self.lang = lang

    def __list_all_cities(self):
        df = pd.read_csv("data/csv/cities.csv", sep=";")
        del df["ID"]
        self.all_cities = df["CITY"].to_list()

    def import_string(self, string):
        lemmatizer = WordNetLemmatizer()
        nlp = spacy.load("fr_core_news_lg" if self.lang ==
                         "fr" else "en_core_web_lg")

        string_tmp = string.lower()

        words = word_tokenize(string_tmp)

        lemmatized_words = [lemmatizer.lemmatize(w) for w in words]
        lemmatized_words = " ".join(lemmatized_words)

        doc = nlp(lemmatized_words)

        return doc

    def import_text(self, source):
        lemmatizer = WordNetLemmatizer()
        nlp = spacy.load("fr_core_news_lg" if self.lang ==
                         "fr" else "en_core_web_lg")

        file = open(source, "r").read().lower()

        words = word_tokenize(file)

        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        lemmatized_words = " ".join(lemmatized_words)

        doc = nlp(lemmatized_words)

        return doc

    def __is_source(self, text):

        return text == "de" or text == "depuis" if self.lang == "fr" else text == "from"

    def __is_destination(self, text):

        return (text == "à" or text == "a" or text == "vers"
                if self.lang == "fr" else text == "to")

    def detect_cities(self, doc):
        cities = {"source": "", "destination": "", "other": ""}

        for idx, token in enumerate(doc):
            if token.pos_ == "PROPN":
                location = token.text.split("-")
                location = " ".join(location).lower()
                if location in self.all_cities:
                    if idx != 0 and self.__is_source(
                            doc[idx - 1].text.lower()):
                        cities["source"] = token.text
                    elif idx != 0 and self.__is_destination(
                            doc[idx - 1].text.lower()):
                        cities["destination"] = token.text
                    else:
                        cities["other"] += "{} ".format(token.text)

        return cities


if __name__ == "__main__":
    # nltk.download('punkt')
    # nltk.download('wordnet')
    NLP = NLP()

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
                "$2",
                " ".join(str(train_station["station"][index_2]).split("-"))))

    print(final_queries[:10])

    for query in final_queries:
        doc = NLP.import_string(query)

        cities = NLP.detect_cities(doc)

        res.append(cities)

    print(res)
    # doc = NLP.import_text("data/txt/text4.txt")

    # cities = NLP.detect_cities(doc)

    # print(cities)
