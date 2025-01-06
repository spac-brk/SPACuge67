import pandas as pd


# Get quartile set based on observations and frequencies
def get_qset(obs):
    cum_obs = obs.cumsum()
    cum_obs /= cum_obs.iloc[-1]
    return (1,
            int((cum_obs >= 0.25).to_numpy().argmax()) + 1,
            int((cum_obs >= 0.5).to_numpy().argmax()) + 1,
            int((cum_obs >= 0.75).to_numpy().argmax()) + 1,
            len(cum_obs))


# Read files
path = "data/"
orders = pd.read_csv(path + "orders_fixed.csv")
products = pd.read_csv(path + "products_fixed.csv")

# Only looking at accepted orders
orders = orders.loc[orders['status'] == 'Accepted']

# Total number of products across all orders
product_counts = orders['product_id'].value_counts().sort_values(ascending=False)
print('\nProduct quartile set:')
print(get_qset(product_counts))

# Total price of products across all orders
product_revenues = pd.DataFrame(product_counts).merge(products, on='product_id')
product_revenues['revenue'] = product_revenues['count'] * product_revenues['price']
product_revenues = product_revenues.set_index('product_id').sort_values(by='revenue',ascending=False)
print('\nRevenue quartile set:')
print(get_qset(product_revenues['revenue']))
