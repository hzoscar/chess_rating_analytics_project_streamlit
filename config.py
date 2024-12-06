# Import the necessary module
from dotenv import load_dotenv
import os
import re

load_dotenv()

# Access environment variables as if they came from the actual environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("Enviroment variable 'DATABASE_URL' is not set.")

if not re.match(r'^postgresql\+psycopg2://\S+:\S+@\S+:\d+/\S+$', DATABASE_URL):
    raise ValueError("The 'DATABASE_URL' is not in the correct format.")

print("The enviroment variable 'DATABASE_URL' was set successfully")

# # Other global constants
# PAGE_TITLE = "Chess Analytics"