import csv
from flask import request, session

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


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