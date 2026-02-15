import csv
from flask import request, session
from flask_socketio import SocketIO, emit
from db_helpers import search_db, alter_db

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


# Validate item before adding to cart
def validate_item(path, item_name):
    """Validate item before adding to cart"""
    item_info = None

    with open(path, "r", encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for item in reader:
            if item_name.strip() == item["name"]:
                item_info = item
    
    if item_info:
        return item_info
    else:
        return "error"


def get_cart_count():
    cart = search_db("cart.db", "SELECT * FROM cart")
    item_count = 0
    for item in cart:
        item_count += int(item["stock"])
    
    return item_count


def update_cart_count(manual_count=None):
    item_count = get_cart_count()
    if manual_count == None and item_count >= 0:        
        emit("display cart item count", item_count)
    else:
        emit("display cart item count", manual_count)


def load_shop(path):
    with open(path, "r", encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        items_list = []
        for item in reader:
            items_list.append(item)

        return items_list


def paginate(items, per_pg):
    pg = request.args.get("pg", 1, type=int)
    start = (pg - 1) * per_pg
    end = start + per_pg
    total_pg = (len(items) + per_pg - 1) // per_pg

    # NOTE: Recall it's 0-indexed
    items_on_pg = items[start:end]

    return [pg, total_pg, items_on_pg]


def process_inventory(img, inputs, shop_info):
    """Finalizes item info before /admin/add-stock route adds it to database"""

    # Save img to folder
    img.save("static/img/shop/" + img.filename)

    # Edit name, price, stock, alt w/ inputs
    for key, value in inputs.items():
        shop_info[key] = value
    
    # Create path for img and convert price into currency format
    shop_info["path"] = "img/shop/" + img.filename
    shop_info["price"] = usd(float(shop_info["price"]))

    # Get header name
    header_names = []
    for key in shop_info:
        header_names.append(key)

    return [header_names, shop_info]


def update_shop(csv_path, header_names_arr, item_info_dict):
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header_names_arr)
        writer.writerow(item_info_dict)


def get_subtotal(cart_arr):
    """Calculate cart subtotal"""
    subtotal = 0
    for item in cart_arr:
        subtotal += float(item["price"]) * int(item["stock"])
    
    return usd(subtotal)


def get_current_stocks(path, cart_arr):
    """Get current stock of items in cart"""
    current_stocks = []

    for item in cart_arr:
        current_stocks.append(validate_item(path, item["name"])["stock"])
    
    return current_stocks


def match_cart_to_shop(cart_item_dict, shop_item_dict):
    """Check if name, price, or stock has changed. If so, update the cart item and create a msg to notify user of change"""
    changed_name = match_shop_field(cart_item_dict, shop_item_dict, "name")
    changed_price = match_shop_field(cart_item_dict, shop_item_dict, "price")
    
    # If desired qty > stock, change qty to highest available stock
    changed_stock = match_shop_stock(cart_item_dict, shop_item_dict)

    if changed_name or changed_price or changed_stock:
        return "NOTICE: Certain items have been updated regarding quantity due to changes in stock, name, and/or price"
    else:
        return None


# Currently, this is only used for item (1) name (2) price 
def match_shop_field(cart_item_dict, shop_item_dict, category):
    if str(cart_item_dict[category]).strip() != str(shop_item_dict[category]).strip():
        alter_db("cart.db", 
            f"UPDATE cart SET {category} = ? WHERE path = ?", 
            (f"{shop_item_dict[category]}", shop_item_dict["path"].strip())
        )
        return True
    
    return False


def match_shop_stock(cart_item_dict, shop_item_dict):
    if int(cart_item_dict["stock"]) > int(shop_item_dict["stock"]):
        alter_db("cart.db", 
                "UPDATE cart SET stock = ? WHERE path = ?", 
                (shop_item_dict["stock"], shop_item_dict["path"].strip())
        )
        return True

    return False


def check_stock(stock, current_qty):
    """"Check if enough stock before adding to cart"""
    if current_qty < stock:
        return True

    return False


def update_dup_cart_item_qty(item_in_db):
    """"If item already in cart, update the qty rather than adding it as new item"""
    cart = search_db("cart.db", "SELECT * FROM cart")
    for product in cart:
        if item_in_db["name"] in product["name"]:
            current_qty, stock = int(product["stock"]), int(item_in_db["stock"])

            # Check if enough stock before updating qty
            if check_stock(stock, current_qty):
                alter_db("cart.db", "UPDATE cart SET stock = ? WHERE name = ?", (product["stock"] + 1, product["name"]))
                return "dup updated"
            else:
                return "not enough stock"
    
    return "no dup found"