import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Create an engine
def get_connection():
    from config import DATABASE_URL
    return create_engine(DATABASE_URL)
    

def test_connection():
        
    try:
        # Create an engine
        engine = get_connection()
        # Test connection
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print("Error: Unable to connect to the database")
        print(e)

def load_data(query):
    engine = get_connection()
    with engine.connect() as conn:
        return pd.read_sql_query(query, conn)


test_connection()








