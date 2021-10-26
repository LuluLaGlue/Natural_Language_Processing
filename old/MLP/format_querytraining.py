import pandas as pd
import random

df = pd.read_csv('data/txt/query.txt', sep=";")
df_2 = pd.read_csv('data/csv/list_train_stations.csv', sep=";")
queries = [[
    "start", "end", "requete", "0", "1", "2", "3", "4", "5", "6", "7", "8",
    "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22"
]]

for (i, q) in enumerate(df["query"]):
    # if q[0] != "#":
    # if i == 0:
    # for s in df_2["station"]:
    #     for s_2 in df_2["station"]:
    #         if s != s_2:
    #             res = [str(s).lower(), str(s_2).lower()]
    #             tmp = q.replace("$1", str(s)).replace(
    #                 "$2", str(s_2)).lower().split(' ')
    #             res.extend(tmp)
    #             queries.append(res)
    # else:
    for v in range(50000):
        index_1 = random.randrange(len(df_2["station"]))
        index_2 = random.randrange(len(df_2["station"]))
        if (df_2["station"][index_1] != df_2["station"][index_2]):
            res = [
                str(df_2["station"][index_1]).lower(),
                str(df_2["station"][index_2]).lower()
            ]
            tmp = q.lower().replace("$1", str(
                df_2["station"][index_1])).replace(
                    "$2", str(df_2["station"][index_2])).split(' ')
            res.extend(tmp)
            queries.append(res)

pd.DataFrame(queries).to_csv("data/csv/training_queries_split_2.csv", sep=";")
