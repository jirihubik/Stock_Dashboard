""" database.py """

import sqlite3
from datetime import datetime

DB_FILE = "tickers.db"

def init_db():
    """Initialize the database if it does not exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickers (
                ticker TEXT PRIMARY KEY,
                company_name TEXT,
                sector TEXT,
                website TEXT,
                country TEXT,
                ipo_date TEXT,
                last_searched TIMESTAMP
            )
        ''')
        conn.commit()

def save_ticker_data(ticker, company_name, sector, website, country, ipo_date):
    """Saves or updates ticker information in the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickers (ticker, company_name, sector, website, country, ipo_date, last_searched)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(ticker) DO UPDATE SET 
                company_name=excluded.company_name,
                sector=excluded.sector,
                website=excluded.website,
                country=excluded.country,
                ipo_date=excluded.ipo_date,
                last_searched=excluded.last_searched
        ''', (ticker, company_name, sector, website, country, ipo_date, datetime.now()))
        conn.commit()


init_db()