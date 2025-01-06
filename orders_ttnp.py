import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)


# Calculate number of days between dates
def delta_calc(dt_first, dt_last):
    dt_first = pd.to_datetime(dt_first)
    dt_last = pd.to_datetime(dt_last)
    return (dt_last - dt_first).dt.days


# Read data into dataframes
path = 'data/'
orders = pd.read_csv(path + 'orders_fixed.csv')

# Only looking at accepted orders
orders = orders.loc[orders['status'] == 'Accepted']

# Find time between purchases per product_id
# Sort by product_id and date
orders = orders.sort_values(['product_id', 'date']).reset_index(drop=True)

# Calculate the date of the next purchase for each product_id
orders['product_next_purchase_date'] = orders.groupby('product_id')['date'].shift(-1)

# Calculate time until next purchase
orders['product_time_to_next_purchase'] = delta_calc(orders['date'], orders['product_next_purchase_date'])

# Drop the temporary 'next_purchase_date' column if only the time difference is needed
orders = orders.drop(columns=['product_next_purchase_date'])

# Statistics on product_time_to_next_purchase
pttnp = orders[(orders['product_time_to_next_purchase'] != 0) &
               (orders['product_time_to_next_purchase'].notna())]
pttnp_mean = pttnp.groupby('product_id')['product_time_to_next_purchase'].mean()
pttnp_std = pttnp.groupby('product_id')['product_time_to_next_purchase'].std()
print('Statistics on product_time_to_next_purchase:')
print('Mean:')
print('Mean ' + str(pttnp_mean.mean()) + ', std ' + str(pttnp_mean.std()))
print('Std:')
print('Mean ' + str(pttnp_std.mean()) + ', std ' + str(pttnp_std.std()))

sns.kdeplot(pttnp_mean,shade=True)
plt.show()

# Find time between purchases per customer_id
# Sort by customer_id and date
orders = orders.sort_values(['customer_id', 'date']).reset_index(drop=True)

# Calculate the date of the next purchase for each customer_id
orders['customer_next_purchase_date'] = orders.groupby('customer_id')['date'].shift(-1)

# Calculate time until next purchase
orders['customer_time_to_next_purchase'] = delta_calc(orders['date'], orders['customer_next_purchase_date'])

# Drop the temporary 'next_purchase_date' column if only the time difference is needed
orders = orders.drop(columns=['customer_next_purchase_date'])

# Statistics on customer_time_to_next_purchase
cttnp = orders[(orders['customer_time_to_next_purchase'] != 0) &
               (orders['customer_time_to_next_purchase'].notna())]
cttnp_mean = cttnp.groupby('customer_id')['customer_time_to_next_purchase'].mean()
cttnp_std = cttnp.groupby('customer_id')['customer_time_to_next_purchase'].std()
print('Statistics on customer_time_to_next_purchase:')
print('Mean ' + str(cttnp_mean.mean()) + ', std ' + str(cttnp_mean.std()))
print('Std:')
print('Mean ' + str(cttnp_std.mean()) + ', std ' + str(cttnp_std.std()))

sns.kdeplot(cttnp_mean,shade=True)
plt.show()

# orders.to_csv(path + 'orders_ttnp.csv')