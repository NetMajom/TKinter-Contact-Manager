from _csv import reader
from sqlite3 import connect

with open('contacts.csv', encoding='utf-8') as file, connect('contacts.db') as conn:
    conn.execute("""CREATE TABLE contacts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name text,
    last_name text,
    email text,
    phone text
    )""")
    conn.executemany("INSERT INTO contacts(first_name, last_name, email, phone) VALUES (?, ?, ?, ?)", reader(file))
