import pandas as pd
import os
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import warnings
warnings.filterwarnings("ignore")


raw_apriori_category_df =pd.read_csv('apriori_category.csv')
raw_apriori_item_df =pd.read_csv('apriori_item.csv')
raw_bestselling_brand_recommendation_df =pd.read_csv('bestselling_brand_recommendation.csv')
raw_bestselling_item_recommendation_df =pd.read_csv('bestselling_item_recommendation.csv')
raw_ratings_brand_recommendation_df =pd.read_csv('ratings_brand_recommendation.csv')
raw_ratings_item_recommendation_df =pd.read_csv('ratings_item_recommendation.csv')

"""Deleting the index column"""
raw_apriori_category_df.drop('Unnamed: 0', axis=1, inplace=True)
raw_apriori_item_df.drop('Unnamed: 0', axis=1, inplace=True)

raw_bestselling_brand_recommendation_df.drop('Unnamed: 0', axis=1, inplace=True)
raw_bestselling_item_recommendation_df.drop('Unnamed: 0', axis=1, inplace=True)

raw_ratings_brand_recommendation_df.drop('Unnamed: 0', axis=1, inplace=True)
raw_ratings_item_recommendation_df.drop('Unnamed: 0', axis=1, inplace=True)

item_category = pd.read_csv("../item_category.csv")

def get_item_category(item_id):
    return item_category[item_category.item_id == f"{item_id}"].values[0][1]

"""let us form DataFrame of Users and the items they have purchased"""
collab_df = pd.read_csv("collab_df.csv",low_memory=False)

"""create pivot table"""
collab_df_pivot = collab_df.pivot(
    index="item_id", columns="user_id", values="rating"
).fillna(0)

"""create sparse matrix to pass to KNN model for training"""
features_df_matrix = csr_matrix(collab_df_pivot.values)

"""creating list of modcloth item_ids"""
item_list = collab_df_pivot.index.tolist()

"""creating KNN model"""
model_knn = NearestNeighbors(metric="cosine", algorithm="brute")

"""fitting the model"""
model_knn.fit(features_df_matrix)


"""Let us build a function which gives 5 nearest neighbours of item"""


def recommender_whole(item_id):
    query_index = np.random.choice(collab_df_pivot.shape[0])
    distances, indices = model_knn.kneighbors(
        collab_df_pivot[collab_df_pivot.index == item_id].values.reshape(1, -1),
        n_neighbors=6,
    )
    nearest_items = [collab_df_pivot.index[i] for i in indices.flatten()[1:]]
    nearest_items_category = [
        item_category[item_category.item_id == item]["category"].values[0]
        for item in nearest_items
    ]
    recommended_items_df = pd.DataFrame(
        {"Recommended_Item": nearest_items, "Category": nearest_items_category}
    )
    return [f"item: {nearest_items[i]} from category: {nearest_items_category[i]}" for i in range(len(nearest_items))]

def rcmnd_item_rating(system_type, category):
    temp_df = raw_ratings_item_recommendation_df[(raw_ratings_item_recommendation_df.Category == category) & (raw_ratings_item_recommendation_df.Recommendation_System_Type == system_type)]
    products = temp_df.Product.tolist()
    brands = temp_df.Brand.tolist()
    ratings = temp_df.Rating.tolist()
    similar_items = [recommender_whole(item) for item in products]
    return products, brands, ratings, similar_items

def rcmnd_brand_rating(system_type, category):
    temp_df = raw_ratings_brand_recommendation_df[(raw_ratings_brand_recommendation_df.Category == category) & (raw_ratings_brand_recommendation_df.Recommendation_System_Type == system_type)]
    brands = temp_df.Brand.tolist()
    ratings = temp_df.Brand_Rating.tolist()
    products = temp_df.Top_Products.tolist()
    return brands, ratings, products

def rcmnd_item_bestseller(system_type, category):
    temp_df = raw_bestselling_item_recommendation_df[
        (raw_bestselling_item_recommendation_df.Category == category)
        & (raw_bestselling_item_recommendation_df.Recommendation_Type == system_type)
    ]
    products = temp_df.Item_ID.tolist()
    brands = temp_df.Brand.tolist()
    quantity = temp_df.Sold_Units.tolist()
    similar_items = [recommender_whole(item) for item in products]
    return products, brands, quantity, similar_items


def rcmnd_brand_bestseller(system_type, category):
    temp_df = raw_bestselling_brand_recommendation_df[
        (raw_bestselling_brand_recommendation_df.Category == category)
        & (raw_bestselling_brand_recommendation_df.Recommendation_System_Type == system_type)
        ]

    brands = temp_df.Brand.tolist()
    quantity = temp_df.Brand_Sales.tolist()
    products = temp_df.Top_Products.tolist()
    return brands, quantity, products


raw_apriori_item_df_itemset = raw_apriori_item_df[["antecedents","consequents","Category"]]
raw_apriori_item_df_itemset["combo"] = raw_apriori_item_df_itemset.antecedents.astype("str") + "," + raw_apriori_item_df_itemset.consequents.astype("str")
combo_item = raw_apriori_item_df_itemset[["Category", "combo"]]

def item_combo_list(category):
    return combo_item[combo_item.Category == category]["combo"].tolist()


combo_category_list = pd.read_csv("category_combo.csv")
combo_category_list = combo_category_list.element.tolist()

def category_combo_list(category):
    """returns list of category combos"""
    combo_list = []
    for combination in combo_category_list:
        if category in combination:
            combo_list.append(combination)
    return combo_list