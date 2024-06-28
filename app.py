from socket import socket
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
from flask_session import Session
from dotenv import load_dotenv
from helpers import *
from db_helpers import search_db, alter_db
import os

SHOP_CSV_PATH = "static/shop.csv"
SHOP_CSV_FIELDNAMES = {
    "name": None,
    "price": None,
    "stock": None,
    "directory": "/static/",
    "path": None,
    "alt": None
}

COLUMN_NAMES = ", ".join(SHOP_CSV_FIELDNAMES.keys())
SQL_PLACEHOLDERS = ", ".join("?" * len(SHOP_CSV_FIELDNAMES))
DB_PATH = "cart.db"

# MSG - let users know if err or cart info change
MSG = None

# Server-side validation for when user selects radio option
RADIO_OPTIONS = ["existing pattern", "own idea"]

app = Flask(__name__)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# USE GEVENT WHEN DEPLOYING
# socketio = SocketIO(app, manage_session=False, async_mode="gevent")
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


@app.route("/request", methods=["GET", "POST"])
def request():
    return render_template("request.html")


@app.route("/order", methods=["GET", "POST"])
def order():
    return render_template("order.html")


@app.route("/cart", methods=["GET", "POST"])
def cart():
    cart = search_db("cart.db", "SELECT * FROM cart")
    if len(cart) > 0:
        # Check if any changes (name, price, available stock) has been changed
        matched_msg = None
        for cart_item in cart:
            # Ensure SQL cart item price are 2 decimal places (esp. whole num prices)
            cart_item["price"] = f'{cart_item["price"]:,.2f}'  
            for shop_item in load_shop(SHOP_CSV_PATH):
                # Chose to compare img path b/c less likely to change compared to name, price, stock
                if cart_item["path"].strip() == shop_item["path"].strip():
                    matched = match_cart_to_shop(cart_item, shop_item)

                    if matched:
                        matched_msg = matched
                        # Update cart since there is changes
                        cart = search_db("cart.db", "SELECT * FROM cart")

        # Load cart item info
        subtotal = get_subtotal(cart)
        current_stocks = get_current_stocks(SHOP_CSV_PATH, cart)
        total_items = get_cart_count()

        return render_template("cart.html", 
            cart_items=cart, 
            current_stocks=current_stocks, 
            total_items=total_items,
            subtotal=subtotal,
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
def display_cart_count(data=None):
    update_cart_count(data)


@socketio.on("add to cart")
def add_to_cart(data):
    item = validate_item(SHOP_CSV_PATH, data)

    if item != "error":
        outcome = update_dup_cart_item_qty(item)
        if outcome == "no dup found":
            # Set desired quantity to 1
            item["stock"] = 1
            # Add the item to cart.db if no dups in cart
            alter_db("cart.db", 
                    f"INSERT INTO cart ({COLUMN_NAMES}) VALUES ({SQL_PLACEHOLDERS})", 
                    tuple(item.values())
            )
            emit("successfully added to cart")
        elif outcome == "dup updated":
            emit("successfully added to cart")
        else:
            emit("not enough stock")

        update_cart_count()
    else:
        emit("error", {
            "ctnr_name": ".shop",
            "index": 0
        })


@socketio.on("delete cart item")
def delete_cart_item(data):
    item = validate_item(SHOP_CSV_PATH, data["name"])
    index = data["index"]
    cart = search_db("cart.db", "SELECT * FROM cart")

    if item != "error":
        for product in cart:
            if data["name"] == product["name"]:
                alter_db("cart.db", "DELETE FROM cart WHERE name = ?", (product["name"],))

        emit("delete cart item", {
            "cart_count": get_cart_count(),
            "index": index
            })
    else:
        emit("error", {
            "ctnr_name": ".cart",
            "index": 1
        })


@socketio.on("update desired qty")
def update_desired_qty(data):
    cart = search_db("cart.db", "SELECT * FROM cart")
    for item in cart:
        if data["name"].strip() == item["name"]:
            alter_db("cart.db", 
                "UPDATE cart SET stock = ? WHERE name = ?", 
                (int(data["newQty"]), item["name"])
            )
            
            emit("refresh pg")
            return True
    
    emit("error", {
        "ctnr_name": ".cart",
        "index": 1
    })


@socketio.on("validate radios")
def validate_radios(data):
    if data["value"] not in RADIO_OPTIONS:
        emit("error", {
            "ctnr_name": ".request-hero",
            "index": 0
        })
    else:
        emit("undisable correct request form element", data["index"])


if __name__ == '__main__':
    socketio.run(app)