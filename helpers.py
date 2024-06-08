import csv
from flask import request, session
from flask_socketio import SocketIO, emit

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


# Validate item before adding to cart
def validate_item(path, item_name):
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
    if "cart" in session:
        item_count = 0
        for item in session["cart"]:
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

    # Recall it's 0-indexed
    items_on_pg = items[start:end]

    return [pg, total_pg, items_on_pg]


# /admin/add-stock
def process_inventory(img, inputs, shop_info):
    # Save img to folder
    img.save("static/img/shop/" + img.filename)

    # Edit name, price, stock, alt w/ inputs
    for key, value in inputs.items():
        shop_info[key] = value
    
    # Create path to img and turn price into currency format
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


# /cart
def get_subtotal(session_arr):
    """Update cart using items stored in session"""
    subtotal = 0
    # Calculate cart subtotal
    for item in session_arr:
        subtotal += float(item["price"].replace("$", "")) * float(item["stock"])
    
    return subtotal


def get_current_stocks(path, session_arr):
    current_stocks = []

    for item in session_arr:
        # Get current stock of items in cart
        current_stocks.append(validate_item(path, item["name"])["stock"])
    
    return current_stocks


def get_total_items(session_arr):
    total_item = 0
    for item in session_arr:
        total_item += int(item["stock"])
    
    return total_item


def match_cart_to_shop(cart_item_dict, shop_item_dict):
    """Check if name, price, or stock has changed. If so, update the cart item and create a msg to notify change"""
    change_one = match_shop_name_price(cart_item_dict, shop_item_dict, "name")
    change_two = match_shop_name_price(cart_item_dict, shop_item_dict, "price")
    
    # If desired qty > stock, change qty to highest available stock
    change_three = match_shop_stock(cart_item_dict, shop_item_dict)

    if change_one or change_two or change_three:
        return "NOTICE: Certain items have been updated regarding quantity due to changes in stock, name, and/or price"
    else:
        return None

    
def match_shop_name_price(cart_item_dict, shop_item_dict, category):
    if cart_item_dict[category].strip() != shop_item_dict[category].strip():
        cart_item_dict[category] = shop_item_dict[category].strip()
        return True
    
    return False


def match_shop_stock(cart_item_dict, shop_item_dict):
    if int(cart_item_dict["stock"]) > int(shop_item_dict["stock"]):
        cart_item_dict["stock"] = int(shop_item_dict["stock"])
        return True

    return False


# for @socketio.on("add to cart")
def check_stock(stock, current_qty):
    """"Check if enough stock before adding to cart"""
    if current_qty < stock:
        return True

    return False


def update_dup_cart_item_qty(item_in_db):
    """"Update cart item qty rather than adding new item if duplicate"""
    for product in session["cart"]:
        if item_in_db["name"] in product["name"]:
            current_qty, stock = int(product["stock"]), int(item_in_db["stock"])

            # Check if enough stock to add more qty
            if check_stock(stock, current_qty):
                product["stock"] = current_qty + 1

                return "dup updated"
            else:
                return "not enough stock"
    
    return "no dup found"