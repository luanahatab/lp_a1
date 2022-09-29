import pandas as pd

df = pd.read_csv("dataframe.csv", index_col=[1,2])

print(df)