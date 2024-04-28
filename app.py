from flask import Flask, render_template, request
from helpers import load_shop, paginate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/shop')
def shop():
    items = load_shop("static/shop.csv")
    pg, total_pg, items_on_pg = paginate(items, 1)
    print(pg, total_pg, items_on_pg)

    return render_template("shop.html", pg=pg, total_pg=total_pg, items_on_pg=items_on_pg)

