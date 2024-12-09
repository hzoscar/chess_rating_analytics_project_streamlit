import pandas as pd
from sqlalchemy import create_engine

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def get_connection_url() -> str:
    """
    Retrieve the database connection URL from the configuration file.
    Returns:
        str: The database connection URL.
    """
    from config import test_credentials
    return test_credentials()


# def test_connection() -> bool:
#     """
#     Test the connection to the database.
#     Returns:
#         bool: True if the connection is successful, False otherwise.
#     """
#     try:
#         # Create an engine and attempt to connect
#         engine = create_engine(get_connection_url())
#         with engine.connect() as connection:
#             print("Connection successful!")
#             return True
#     except SQLAlchemyError as e:
#         print("Error: Unable to connect to the database")
#         print(f"Details: {e}")
#         return False

def load_data(query: str) -> pd.DataFrame:
    """
    Test the connection to the database, then execute a SQL query and return the results as a pandas DataFrame.
    Args:
        query (str): The SQL query to execute.
    Returns:
        pd.DataFrame: Query results as a DataFrame.
    Raises:
        RuntimeError: If the database connection cannot be established or the query fails.
    """
    try:
        # Create the engine and execute the query
        engine = create_engine(get_connection_url())
        with engine.connect() as conn:
            print("Connection successful!")
            # Execute the query
            return pd.read_sql_query(query, conn)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database connection or query execution failed: {e}")










