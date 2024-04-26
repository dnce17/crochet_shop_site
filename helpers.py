import csv

def load_shop(path):
    with open(path, "r", encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        items_list = []
        for item in reader:
            items_list.append(item)

        return items_list