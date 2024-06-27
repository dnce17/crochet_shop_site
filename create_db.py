import sqlite3

con = sqlite3.connect("cart.db")
db = con.cursor()

create_cart = db.execute("""CREATE TABLE cart (
                                id INTEGER NOT NULL,
                                name TEXT NOT NULL,
                                price NUMERIC DEFAULT 0,
                                stock INTEGER NOT NULL DEFAULT 1,
                                directory TEXT NOT NULL,
                                path TEXT NOT NULL,
                                alt TEXT NOT NULL,
                                PRIMARY KEY(id)
                              )"""
                          )

