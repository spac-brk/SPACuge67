from collections import defaultdict
import pandas as pd
import ast
import json
import pprint

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)


# Parse hierarchical categories and separate by levels
def parse_category_hierarchy(categories_str):
    # Convert the category string representation to a list of lists
    categories = ast.literal_eval('[' + categories_str + ']')
    # Create a list of dictionaries with hierarchical levels as keys
    parsed_categories = []
    for path in categories:
        level_dict = {}
        for i, level in enumerate(path):
            level_dict[f'category_level_{i + 1}'] = level
        parsed_categories.append(level_dict)
    return parsed_categories


# Create a recursive nested defaultdict
def nested_dict():
    return defaultdict(nested_dict)


# Convert defaultdicts to regular dictionaries for readability
def convert_to_regular_dict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_to_regular_dict(v) for k, v in d.items()}
    return d


# Read data into dataframes
path = 'data/'
products = pd.read_csv(path + 'products_fixed.csv')

# Apply parsing function to each row in Products
products['parsed_categories'] = products['categories'].apply(parse_category_hierarchy)

# Explode the parsed categories so each product_id has multiple rows, one for each hierarchy path
categories_expanded = products.explode('parsed_categories').reset_index(drop=True)

# Add a column with an incrementing integer per `product_id`
categories_expanded['product_hierarchy_index'] = categories_expanded.groupby('product_id').cumcount()

# Convert each dictionary of hierarchical levels into separate columns
category_levels = pd.json_normalize(categories_expanded['parsed_categories'])
categories_expanded = pd.concat([categories_expanded.drop(columns=['parsed_categories']), category_levels], axis=1)

# Output from expanded categories
categories_expanded.to_csv(path + 'products_cats.csv', index=False)
# print("Products with Separated Category Levels:")
# print(categories_expanded)

# Dataset with unique category hierarchies
all_cat_levels = ['category_level_' + str(x + 1) for x in range(7)]
unique_cat_exp = (categories_expanded[all_cat_levels]
                  .drop_duplicates()
                  .sort_values(by=all_cat_levels)
                  .reset_index(drop=True))


# Create the nested dictionary
category_tree = nested_dict()
for _, row in unique_cat_exp.iterrows():
    current_level = category_tree
    for level in row:
        if pd.notna(level):
             current_level = current_level.setdefault(level, nested_dict())
        else:
            current_level[None] = {}
            break

# Convert and display the nested dictionary
category_tree = convert_to_regular_dict(category_tree)
with open(path + 'category_tree.json', 'w') as f:
    f.write(json.dumps(category_tree,indent=4))
pprint.pp(category_tree)

# Output from unique categories
unique_cat_exp.to_csv(path + 'unique_categories.csv', index=False)
print('\nUnique category hierarchies:')
print(unique_cat_exp)
print('Number of rows at each level:')
for i in all_cat_levels:
    print(len(unique_cat_exp[i].value_counts().values.tolist()))

