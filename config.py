import os

postresql_password = os.getenv('postresql_password')
DB_CONFIG = {
    "host": "localhost",
    "database": "db_fide_100",
    "user": "postgres",
    "password": os.getenv 
}

# Other global constants
PAGE_TITLE = "Chess Analytics"