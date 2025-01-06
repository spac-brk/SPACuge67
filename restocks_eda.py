import pandas as pd

path = "data/"
df = pd.read_csv(path + "restocks.csv")

df = df.drop('amount', axis=1)

df["shipping time"] = (pd.to_datetime(df["delivery_date"])-pd.to_datetime(df["order_date"])).dt.days

df.to_csv(path + "restocks_fixed.csv", index = False)