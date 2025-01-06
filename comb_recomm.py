import pandas as pd
from itertools import combinations
from collections import Counter

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)


# Function to recommend product combinations
def recommend_combinations(products, combination_df, top_n=3):
    """
    Recommend additional products frequently bought together with the given products.
    :param products: List of products to check combinations for.
    :param combination_df: DataFrame containing product combinations and their frequencies.
    :param top_n: Number of top combinations to recommend.
    :return: DataFrame with recommendations.
    """
    recommendations = combination_df[combination_df['product_combination'].apply(
        lambda comb: all(p in comb for p in products) and len(comb) > len(products))]

    # Sort by frequency and return the top N recommendations
    return recommendations.head(top_n)


# Recommendation Function
def recommend_combinations_conf(products, combination_df, top_n=3):
    """
    Recommend additional products frequently bought together with the given products.
    :param products: List of products to check combinations for.
    :param combination_df: DataFrame containing product combinations and their confidence.
    :param top_n: Number of top recommendations to return.
    :return: DataFrame with recommendations.
    """
    recommendations = combination_df[
        combination_df['base_combination'] == tuple(sorted(products))
    ]
    return recommendations[['product_combination', 'confidence']].head(top_n)



# Read data into dataframes
path = 'data/'
orders = pd.read_csv(path + 'orders_fixed.csv')

# Only looking at accepted orders
orders = orders.loc[orders['status'] == 'Accepted']

# Find all combinations of products in each order, for lengths 2 to max(products in order)
order_groups = orders.groupby('order_id')['product_id'].apply(list)

# Generate combinations of varying lengths
product_combinations = []
for products in order_groups:
    for r in range(2, len(products) + 1):  # Varying lengths: from 2 to the total number of products
        product_combinations.extend(combinations(sorted(products), r))

# Count the frequency of each combination
combination_counts = Counter(product_combinations)

# Convert to a DataFrame for analysis
combination_df = pd.DataFrame(combination_counts.items(), columns=['product_combination', 'frequency'])
combination_df = combination_df.sort_values(by='frequency', ascending=False).reset_index(drop=True)

print("Product Combinations with Frequency:")
print(combination_df)

combination_df.to_csv(path + 'combination_recommendations.csv', index=False)

# *** Normalize by total number of orders with product_id ***
# Count the total occurrences of each individual product
product_counts = orders['product_id'].value_counts()

# Expand the combination counts into rows, treating each product as a base
rows = []
for comb, freq in combination_counts.items():
    for product in comb:
        # Treat each product in the combination as the base
        base_frequency = product_counts[product]
        confidence = freq / base_frequency
        rows.append({'product_combination': comb,
                     'base_product': product,
                     'frequency': freq,
                     'base_frequency': base_frequency,
                     'confidence': confidence})

# Create a DataFrame for recommendations
combination_df = pd.DataFrame(rows).sort_values(by='confidence', ascending=False).reset_index(drop=True)
filt_comb_df = combination_df.loc[combination_df['base_frequency'] >= 10]

print("Product Combinations with Confidence:")
print(filt_comb_df)

filt_comb_df.to_csv(path + 'filt_comb_recomm.csv', index=False)


