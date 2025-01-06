import pandas as pd
import numpy as np

path = "data/"

df = pd.read_csv(path + "orders.csv")

df["order_id"] = np.arange(1, len(df) + 1)

df.to_csv(path + 'orders_id.csv', index = False)

df = df.drop('price', axis=1)

df = df.rename(columns={'products': 'product_id'})

# Step 1: Remove trailing commas and spaces, then split into lists
df['product_id'] = df['product_id'].str.strip(", ").str.split(", ")

# Step 2: Use explode to expand each product code into separate rows
df = df.explode('product_id', ignore_index=True)

df.to_csv(path + "orders_fixed.csv", index = False)

df2 = df[['order_id','product_id']]

df2.to_csv(path + 'orders_products.csv', index = False)