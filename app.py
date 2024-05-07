from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
from flask_session import Session
import os
from dotenv import load_dotenv
from helpers import load_shop, paginate, process_inventory, update_shop, usd, validate_item

SHOP_CSV_PATH = "static/shop.csv"
SHOP_CSV_FIELDNAMES = {
    "name": None,
    "price": None,
    "stock": None,
    "directory": "/static/",
    "path": None,
    "alt": None
}

app = Flask(__name__)

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
    subtotal = 0

    # Calculate subtotal of cart
    if "cart" in session:
        for item in session["cart"]:
            subtotal += float(item["price"].replace("$", ""))
            
        return render_template("cart.html", cart_items=session["cart"], subtotal=usd(subtotal))
    
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
@socketio.on("add to cart")
def add_to_cart(data):
    item = validate_item(SHOP_CSV_PATH, data)
    if item != "error":

        def check_dup_cart_items(item_in_db):
            for product in session["cart"]:
                if item_in_db["name"] in product["name"]:
                    qty = int(product["stock"])
                    print("Qty: " + str(qty))
                    product["stock"] = qty + 1

                    print("dup item found and updated")
                    return True
            
            return False
        
        check_dup_cart_items(item)

        # TODO: apply this assuming the item has no dups in cart
        # session["cart"].append(item)

        # Addresses issue of arr items getting deleted upon refresh
        # when appending to item using websocket
        session["cart"] = session["cart"]
        print(session["cart"])
    else:
        print("ADD LATER: create some error msg asking user to refresh page")


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
        print("ADD LATER: create some error msg asking user to refresh page")



if __name__ == '__main__':
    socketio.run(app)