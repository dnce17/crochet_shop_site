import csv
from flask import request

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