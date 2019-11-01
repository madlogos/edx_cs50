# -*- coding: UTF-8 -*-
import os
from sqlalchemy import create_engine
import pandas as pd

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
conn = engine.connect()

# create tables
conn.execute("""
    CREATE TABLE IF NOT EXISTS book (
        id SERIAL PRIMARY KEY,
        isbn VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        author VARCHAR NOT NULL,
        year INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS mbr (
        id SERIAL PRIMARY KEY,
        username VARCHAR NOT NULL,
        pwd VARCHAR NOT NULL
    );
    CREATE TABLE IF NOT EXISTS review (
        id SERIAL PRIMARY KEY,
        rev_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
        mbr_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        rating INTEGER,
        review VARCHAR
    );
""")

df = pd.read_csv("books.csv")
df.to_sql("book", con=conn, if_exists="append", index=False)

conn.close()
