from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
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
socketio = SocketIO(app)


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


@app.route("/order", methods=["GET", "POST"])
def order():
    return render_template("order.html")


@app.route("/cart", methods=["GET", "POST"])
def cart():
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
    validate_item(SHOP_CSV_PATH, data)
