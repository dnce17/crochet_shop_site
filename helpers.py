import csv
from flask import request, session

# REUSABLE
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
        print("item located in db")
        return item_info
    else:
        return "error"


# SINGLE-USE (at least so far)
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
        subtotal += float(item["price"].replace("$", ""))
    
    return subtotal


def get_current_stocks(path, session_arr):
    current_stocks = []

    for item in session_arr:
        # Get current stock of items in cart
        current_stocks.append(validate_item(path, item["name"])["stock"])
    
    print("Current Stock: " + str(current_stocks))
    return current_stocks

def get_total_items(session_arr):
    total_item = 0
    for item in session_arr:
        total_item += int(item["stock"])
    
    print(total_item)
    return total_item