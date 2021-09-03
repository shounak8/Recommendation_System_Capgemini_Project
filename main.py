from flask import Flask, redirect, render_template
from database import rcmnd_item_rating, rcmnd_brand_rating, rcmnd_brand_bestseller, rcmnd_item_bestseller, item_combo_list, category_combo_list
import os
import pandas

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/methodology")
def methodology():
    return render_template("methodology.html")


@app.route("/conclusion")
def conclusion():
    return render_template("conclusion.html")


@app.route("/content")
def content():
    path = "static/images/categories/"
    os.chdir(path)
    cat_img_list = (os.listdir())
    os.chdir("../../..")
    cat_list = [img.split(".")[0] for img in cat_img_list]
    # print(cat_img_list)
    return render_template("content.html", cat_list=cat_list, cat_img_list=cat_img_list)


@app.route("/rating/<cat>", methods=["GET","POST"])
def best_rated(cat):
    cat = cat.split(".")[0]
    best_rated_items_overall = rcmnd_item_rating(system_type="Overall Rating", category=cat)
    best_rated_items_trend = rcmnd_item_rating(system_type="Latest Trend Rating", category=cat)
    best_rated_brand_overall = rcmnd_brand_rating(system_type="Overall_Brandwise_Recommendation", category=cat)
    best_rated_brand_trend = rcmnd_brand_rating(system_type="Latest_Brandwise_Recommendation", category=cat)
    return render_template("best_rated.html",cat=cat, best_rated_items_overall=best_rated_items_overall,
                           best_rated_items_trend=best_rated_items_trend,
                           best_rated_brand_overall=best_rated_brand_overall,
                           best_rated_brand_trend=best_rated_brand_trend)

@app.route("/sales/<cat>", methods=["GET","POST"])
def best_selling(cat):
    cat = cat.split(".")[0]
    bestselling_items_overall = rcmnd_item_bestseller(system_type="Overall_Bestselling_Items", category=cat)
    bestselling_items_trend = rcmnd_item_bestseller(system_type="Latest_Bestselling_Items", category=cat)
    bestselling_brand_overall = rcmnd_brand_bestseller(system_type="Overall_Bestselling_Brand", category=cat)
    bestselling_brand_trend = rcmnd_brand_bestseller(system_type="Latest_Bestselling_Brand", category=cat)
    return render_template("best_selling.html",cat=cat, bestselling_items_overall=bestselling_items_overall,bestselling_items_trend=bestselling_items_trend,
                           bestselling_brand_overall=bestselling_brand_overall, bestselling_brand_trend=bestselling_brand_trend)

@app.route("/combos/<cat>")
def combos(cat):
    cat = cat.split(".")[0]
    items = item_combo_list(cat)
    items = [i.split(",") for i in items]
    categories = category_combo_list(cat)
    # print(categories)
    # print(cat)
    return render_template("combos.html",cat=cat, items=items, categories=categories, enumerate=enumerate)


if __name__ == "__main__":
    app.run(debug=True)
