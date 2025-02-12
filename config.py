from dotenv import load_dotenv
import os
import re

load_dotenv()

def test_credentials() -> str:
    """
    Validates and retrieves the 'DATABASE_URL' environment variable.
    Returns:
        str: The validated 'DATABASE_URL'.
    Raises:
        ValueError: If the 'DATABASE_URL' is not set or is incorrectly formatted.
    """
    # Fetch the environment variable
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        raise ValueError("Environment variable 'DATABASE_URL' is not set.")

    # Regex to validate the PostgreSQL connection string
    pattern = r'^postgresql\+psycopg2://\S+:\S+@\S+:\d+/\S+$'
    if not re.match(pattern, database_url):
        raise ValueError(
            "The 'DATABASE_URL' is not in the correct format. Expected format: "
            "'postgresql+psycopg2://username:password@host:port/database'"
        )

    return database_url

import streamlit as st
from supabase import create_client, Client

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()