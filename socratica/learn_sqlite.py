import sqlite3

conn = sqlite3.connect("D\\demo\\appha.db")



cur = conn.cursor()

conn.execute('''CREATE TABLE IF NOT EXISTS people
             (first_name TEXT, last_name Text)''')

# test data

names_list = [
    ("Roderick", "Watson"),
    ("Roger", "Hom"),
    ("Petri", "Halonen"),
    ("Jussi", ""),
    ("James", "McCann")

]

# Insert data into database

cur.executemany('''
        INSERT INTO people (first_name, last_name) VALUES (?, ?)
    ''', names_list)
conn.commit()

cur.close()
conn.close()