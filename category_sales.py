import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)

# Read data into dataframes
path = 'data/'
orders = pd.read_csv(path + 'orders_fixed.csv')
products = pd.read_csv(path + 'products_fixed.csv')
# restocks = pd.read_csv(path + 'restocks_fixed.csv')
# start_inventory = pd.read_csv(path + 'start_inventory.csv')
categories_expanded = pd.read_csv(path + 'products_cats.csv', dtype=str)

# Only looking at accepted orders
orders = orders.loc[orders['status'] == 'Accepted']

# Merge Orders with Product and Category Data
sales_data = orders.merge(products[['product_id', 'name', 'price']], on='product_id')
sales_data['revenue'] = sales_data['price']

# Calculate Total Sales by Customer
customer_sales = sales_data.groupby(['customer_id', 'name']).agg({
    'order_id': 'count',  # Total orders per product
    'revenue': 'sum'  # Total revenue per product
}).rename(columns={'order_id': 'total_orders'}).reset_index()

# Calculate Total Sales by Product
product_sales = sales_data.groupby(['product_id', 'name']).agg({
    'order_id': 'count',  # Total orders per product
    'revenue': 'sum'  # Total revenue per product
}).rename(columns={'order_id': 'total_orders'}).reset_index()

# Merge Sales Data with Separated Category Levels
sales_by_category_levels = sales_data.merge(categories_expanded, on='product_id')

# Sales by top category level
sales_by_level_1 = sales_by_category_levels.groupby('category_level_1').agg({
    'order_id': 'count',  # Total orders per top-level category
    'revenue': 'sum'  # Total revenue per top-level category
}).rename(columns={'order_id': 'total_orders'}).reset_index()

print("\nTotal Sales by Top Level Category:")
print(sales_by_level_1)
sales_by_level_1.to_csv(
    path + 'category_level_1_sales.csv', )

# Sales by second category level, if applicable
if 'category_level_2' in sales_by_category_levels.columns:
    sales_by_level_2 = sales_by_category_levels.groupby(['category_level_1',
                                                         'category_level_2']).agg({
        'order_id': 'count',
        'revenue': 'sum'
    }).rename(columns={'order_id': 'total_orders'}).reset_index()

    print("\nTotal Sales by Second Level Category:")
    print(sales_by_level_2)
    sales_by_level_2.to_csv(
        path + 'category_level_2_sales.csv',)

# Sales by third category level, if applicable
if 'category_level_3' in sales_by_category_levels.columns:
    sales_by_level_3 = sales_by_category_levels.groupby(['category_level_1',
                                                         'category_level_2',
                                                         'category_level_3']).agg({
        'order_id': 'count',
        'revenue': 'sum'
    }).rename(columns={'order_id': 'total_orders'}).reset_index()

    print("\nTotal Sales by Third Level Category:")
    print(sales_by_level_3)
    sales_by_level_3.to_csv(
        path + 'category_level_3_sales.csv',)