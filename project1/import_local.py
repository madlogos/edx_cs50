# -*- coding: UTF-8 -*-
# create sqlite3 tables if cannot use remote postgres db
import os
import sqlite3
import pandas as pd

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
conn = sqlite3.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# create tables
cur.execute("""
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        isbn TEXT NOT NULL,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL
    );""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS mbr (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        pwd TEXT NOT NULL
    );""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS review (
        id INTEGER PRIMARY KEY,
        rev_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
        mbr_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        rating INTEGER,
        review TEXT
    );""")

if cur.execute('select count(*) from book;').fetchone()[0] == 0:
    df = pd.read_csv(r'H:\data\projects\web\cs50_proj1\books.csv')
    df.to_sql(name='book', con=conn, if_exists='append', index=False)

cur.close()
conn.close()