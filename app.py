from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
from flask_session import Session
import os
from dotenv import load_dotenv
from helpers import *

SHOP_CSV_PATH = "static/shop.csv"
SHOP_CSV_FIELDNAMES = {
    "name": None,
    "price": None,
    "stock": None,
    "directory": "/static/",
    "path": None,
    "alt": None
}

# MSG - let users know if err or cart info change
MSG = None

app = Flask(__name__)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app, manage_session=False)

# Load vars from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/shop')
def shop():
    # Create cart if does not exist
    if "cart" not in session:
        session["cart"] = []
        print("New cart made")
    
    print(session["cart"])

    # Load shop items from CSV file
    items = load_shop(SHOP_CSV_PATH)

    # Placeholders used to show how shop.html looks; will leave in for display purposes
    for _ in range(0, 100):
        placeholder = {
            'name': 'PLACEHOLDER', 
            'price': '$??.??', 
            'stock': '1', 
            'directory': '', 
            'path': 'https://placehold.co/330x330',
            'alt': 'placeholder'
        }
        items.append(placeholder)

    pg, total_pg, items_on_pg = paginate(items, 24)

    return render_template("shop.html", pg=pg, total_pg=total_pg, items_on_pg=items_on_pg)


@app.route("/order", methods=["GET", "POST"])
def order():
    return render_template("order.html")


@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "cart" in session:
        # Check if any changes (name, price, available stock) has been changed
        matched_msg = None
        for cart_item in session["cart"]:
            for shop_item in load_shop(SHOP_CSV_PATH):
                # Chose to compare img path b/c less likely to change compared to name, price, stock, if needed
                if cart_item["path"].strip() == shop_item["path"].strip():
                    matched = match_cart_to_shop(cart_item, shop_item)

                    if matched:
                        matched_msg = matched

        # Load cart item info
        subtotal = get_subtotal(session["cart"])
        current_stocks = get_current_stocks(SHOP_CSV_PATH, session["cart"])
        total_items = get_total_items(session["cart"])

        return render_template("cart.html", 
            cart_items=session["cart"], 
            current_stocks=current_stocks, 
            total_items=total_items,
            subtotal=usd(subtotal),
            matched_msg=matched_msg
        )
    
    return render_template("cart.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


# Will consider making it only accessible by admin later on
@app.route('/admin/add-stock', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Error checking
        img = request.files["img"]
        if not img:
            return "No image uploaded"
            
        inputs = request.form
        for _, value in inputs.items():
            if value == "":
                return "Ensure all fields are filled out"

        # Save img to folder and create info to add to CSV
        header_names, shop_info = process_inventory(img, inputs, SHOP_CSV_FIELDNAMES.copy())

        # Add to CSV
        update_shop(SHOP_CSV_PATH, header_names, shop_info)    

    return render_template("add-stock.html")


# flask-socketio
@socketio.on("display cart item count")
def display_cart_count():
    update_cart_count()


@socketio.on("add to cart")
def add_to_cart(data):
    item = validate_item(SHOP_CSV_PATH, data)
    if item != "error":
        print("success add to cart")
        if update_dup_cart_item_qty(item) == False:
            # Set desired quantity to 1
            item["stock"] = 1
            # TODO: append the item if no dups in cart
            session["cart"].append(item)

        # Addresses issue of arr items getting deleted upon refresh
        # when appending to item using websocket
        session["cart"] = session["cart"]
        print(session["cart"])

        update_cart_count()
    else:
        print("ADD LATER: create some error msg asking user to refresh page")
        emit("error", {
            "ctnr_name": ".shop",
            "index": 0
        })


@socketio.on("delete cart item")
def delete_cart_item(data):
    item = validate_item(SHOP_CSV_PATH, data["name"])
    index = data["index"]

    if item != "error":
        for product in session["cart"]:
            if data["name"] == product["name"]:
                session["cart"].remove(product)

        session["cart"] = session["cart"]

        print(session["cart"])
        print(index)
        emit("delete cart item", index)
    else:
        emit("error", {
            "ctnr_name": ".cart",
            "index": 1
        })


@socketio.on("update desired qty")
def update_desired_qty(data):
    for item in session["cart"]:
        if data["name"].strip() == item["name"]:
            # CAUTION to self: Don't forget to convert str to int or else
            # new qty not display correctly OR convert str to int in HTML itself
            item["stock"] = int(data["newQty"])
            session["cart"] = session["cart"]
            
            emit("refresh pg")
            return True
    
    emit("error", {
        "ctnr_name": ".cart",
        "index": 1
    })


if __name__ == '__main__':
    socketio.run(app)