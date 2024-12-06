import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Database Connection
def get_connection():
    from config import DB_CONFIG
    return psycopg2.connect(
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )

# Load Data from Query
def load_data(query):
    conn = get_connection()
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()
