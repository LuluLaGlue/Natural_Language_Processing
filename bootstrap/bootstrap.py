import nltk
import pathlib
import tensorflow as tf
from bunch import Bunch
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("stopwords")

wcss = []
b = Bunch()
vectorizer = TfidfVectorizer()
lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words("french"))
data_dir = pathlib.Path('discours/tous/*')
filenames = tf.io.gfile.glob(str(data_dir))
data = []

for file in filenames:
    filtered_list = []

    text = open(file, 'r').read().replace('\n', ' ').lower()
    tokenized_string = word_tokenize(text)
    lemmatized_words = [
        lemmatizer.lemmatize(word) for word in tokenized_string
    ]

    for word in lemmatized_words:

        if word.casefold() not in stop_words:
            filtered_list.append(word)

    data.append(' '.join(filtered_list))

b.filenames = filenames
b.content = data
b.dict = Bunch()

for index, file in enumerate(b.filenames):
    b.dict[file] = b.content[index][:40]

b.tf_idf = Bunch()

b.tf_idf = vectorizer.fit_transform(b.content)
print(b.tf_idf.shape)

true_k = 2
model = KMeans(n_clusters=true_k, init='k-means++', n_init=1)
history = model.fit_transform(b.tf_idf)

p = vectorizer.transform([b.dict[list(b.dict.keys())[0]]])

pred = model.predict(p)
print("Prediction for {}: {}".format(list(b.dict.keys())[0], pred[0]))
