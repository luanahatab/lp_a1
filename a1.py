import pandas as pd

df = pd.read_csv("dataframe.csv", index_col=[0,1])

print(df)