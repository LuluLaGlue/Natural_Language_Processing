import pandas as pd


def loop(first, df):
    for (i, v) in enumerate([
            first, "requete", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
            15, 16, 17, 18, 19, 20, 21, 22, 23
    ]):
        df[str(v)] = pd.Categorical(df[str(v)])
        df[str(v)] = df[str(v)].cat.codes
    return df


df_end = pd.read_csv('data/csv/training_queries_split_2.csv', sep=";")
df_start = pd.DataFrame(df_end)

df_end.pop("id")
df_start.pop("id")

df_end.pop("start")
df_start.pop("end")

df_start = loop("start", df_start)
df_end = loop("end", df_end)

df_end.to_csv("./data/csv/training_queries_end_2.csv", sep=";")
df_start.to_csv("./data/csv/training_queries_start_2.csv", sep=";")