import pandas as pd
from shutil import get_terminal_size
pd.set_option('display.width', get_terminal_size()[0])
pd.set_option('display.max_columns', None)


path = "data/"
df = pd.read_csv(path + "products.csv")

df = df.rename({"id": "product_id", "brand": "supplier"}, axis = 1)

df = df.drop('description', axis=1)
df = df.drop('im_url', axis=1)

df["price"] = pd.to_numeric(df["price"])

df["categories"] = (df["categories"]
                    .str.replace(r'Women"s', "Women's", regex=False)
                    .str.replace(r'Men"s', "Men's", regex=False))

df['name'] = (df['name'].str.replace(r'\r', '', regex=True)
                        .str.replace(r'\n', '', regex=True))

df.to_csv(path + "products_fixed.csv", index = False)