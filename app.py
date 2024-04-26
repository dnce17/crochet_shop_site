from flask import Flask, render_template
from helpers import load_shop

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/shop')
def shop():
    items = load_shop("static/shop.csv")
    return render_template("shop.html", items=items)

