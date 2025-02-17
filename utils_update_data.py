import pandas as pd
from sqlalchemy import create_engine, select, Table, MetaData, text
from sqlalchemy.exc import SQLAlchemyError
import zipfile
import os
from datetime import datetime
import warnings
from google.cloud import storage
from utils_pages import get_connection_url
warnings.filterwarnings('ignore')

###################################################
# Conection database
###################################################

def download_from_gcs(bucket_name, source_blob_name, destination_file_name):
    """Download a file from GCS to a local directory for processing."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"File {source_blob_name} downloaded from {bucket_name} to {destination_file_name}")

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
            df = pd.read_sql_query(query, conn)
            
            if 'date' in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            
            return df
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database connection or query execution failed: {e}")
    
###################################################
# Extraction files
###################################################
    
def extract_zip(zip_files, folder_path):
    # List all zip files in the folder
    for file in zip_files:
        with zipfile.ZipFile(os.path.join(folder_path, file), 'r') as zip_ref:
            zip_ref.extractall(folder_path)
            print(f'{file} extracted successfully')
            
###################################################
# Check integrity dataset loaded
###################################################

def is_null(df,column):
    # Check if a column contains null values
    total_null_values = df[column].isnull().sum()
    if total_null_values > 0:
        print(f'The column {column} contains {total_null_values} null values')
        return True
    else:
        print(f'The column {column} does not contain null values')
        return False            

# Function to check if a column contains only numeric values
def is_numeric_column(df,column):
    try:
        pd.to_numeric(df[column])
        print(f'The column {column} is numeric')
        return True
        
    except ValueError:
        print(f'The column {column} contains not numeric values')
        return False
        
def max_and_min_length(df, column):
    # Get the maximum and minimum length of the columns
    lengths = df[column].astype('str').str.len()
    max_length = lengths.max()
    min_length = lengths.min()    
    print(f'The minimum and maximum length of column {column} is {min_length} and {max_length} respectively')
    
    return min_length, max_length

# Function to check if a column does not contain numeric values or alphanumeric strings
def contains_numeric_values(df,column):
    if df[column].astype('str').str.contains(r'\d').any():
        print(f'The column {column} contains numeric values')
        return True
    else:
        print(f'The column {column} does not contain numeric values')
        return False

def check_column(df, column_name, is_numeric=False, contains_no_numbers=False, min_length=None, max_length=None):
    """
    General function to check and validate a column in a DataFrame.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to check.
        column_name (str): The name of the column to validate.
        is_numeric (bool): If True, check if the column contains only numeric values.
        contains_no_numbers (bool): If True, check if the column does not contain numeric values.
        min_length (int): Minimum allowed length of values in the column.
        max_length (int): Maximum allowed length of values in the column.
    """
    # Check for null values
    null_check = is_null(df, column_name)
    if null_check:
    #    df.dropna(subset=[column_name], inplace=True)
        print(f"**Handle null values in column {column_name}")
    # Check if the column should contain only numeric values
    if is_numeric:
        numeric_check = is_numeric_column(df, column_name)
        if not numeric_check:
            print(f"**Verify values in column {column_name}: not all are numeric.")
    
    # Check if the column should not contain numeric values
    if contains_no_numbers:
        contains_numeric_values_check = contains_numeric_values(df, column_name)
        if contains_numeric_values_check:
            print(f"**Verify values in column {column_name}: contains numeric values.")
    
    # Check for length constraints
    if min_length is not None or max_length is not None:
        min_length_val, max_length_val = max_and_min_length(df, column_name)
        if min_length is not None and min_length_val < min_length:
            print(f"**Verify values in column {column_name}: minimum length is below {min_length}.")
        if max_length is not None and max_length_val > max_length:
            print(f"**Verify values in column {column_name}: maximum length exceeds {max_length}.")
            
def check_country_code(df):
    query = """
    SELECT distinct  c.code
    FROM countries c
    """
    df_historic_fed = load_data(query)
    historic_fed_list = df_historic_fed['code'].to_list()
    check_codes = df[~df['Fed'].isin(historic_fed_list)]['Fed'].unique()
    if len(check_codes) > 0:
        print(f'** The following country codes are not in the database country codes list: {check_codes}')
    else:
        print('All country codes are in the database country codes list')
        
###################################################
# Preprocessing data
###################################################

def add_column_date(df, rating_column):
    df['Year'] = int('20' + (rating_column[0][-2:]))
    df['Month'] = rating_column[0][:3]
    # Convert "Month" to numeric month format
    df['Month'] = df['Month'].apply(lambda x: datetime.strptime(x, '%b').month)

    # Create a new column with a date format
    df['Date'] = (pd.to_datetime(df[['Year', 'Month']].assign(Day=1))) #+ pd.offsets.MonthEnd(0))
    
    #df['Date'] = df['Date'] + pd.DateOffset(months=1)
    
    df.drop(['Month','Year'],axis=1,inplace=True)
    return df

def clean_df(df):    
    df.dropna(subset=['ID','Name','Fed','Sex','B-day','Rating'], inplace=True)
    df['Title'] = df['Title'].fillna('NT')
    df['Number_of_games'] = df['Number_of_games'].fillna(0)
    df['activity_status'] = df['activity_status'].fillna('a') 
    df['activity_status']= df['activity_status'].replace({'w':'a','wi':'i'})
    # df[(df['Name'].str.contains(r'\d'))]
    #df[df['B-day'].astype('str').str.len() != 4]
    return df

def clean_names(df):
    # Extract name part before numbers or parentheses
    pattern = r'^([A-Za-z,.\' `/\-]*?)(?=[\d\(]|$)'
    df['Name'] = df['Name'].str.extract(pattern)[0]
    
    # Clean trailing spaces and special chars
    df['Name'] = df['Name'].str.strip(' -`/')
    
    return df

def replace_wrongcountry_code_with_right_country_code(df):
    dict_to_map = {'ALG': 'DZA',
        'ANG': 'AGO',
        'ARU': 'ABW',
        'BAH': 'BHS',
        'BAN': 'BGD',
        'BAR': 'BRB',
        'BER': 'BMU',
        'BHU': 'BTN',
        'BOT': 'BWA',
        'BRN': 'BHR',
        'BRU': 'BRN',
        'BUL': 'BGR',
        'BUR': 'BFA',
        'CAM': 'KHM',
        'CHI': 'CHL',
        'CRC': 'CRI',
        'CRO': 'HRV',
        'DEN': 'DNK',
        'GAM': 'GMB',
        'GER': 'DEU',
        'GRE': 'GRC',
        'GUA': 'GTM',
        'HAI': 'HTI',
        'HON': 'HND',
        'ESA': 'SLV',
        'FAI': 'FRO',
        'FIJ': 'FJI',
        'GCI': 'GGY',
        'INA': 'IDN',
        'IRI': 'IRN',
        'ISV': 'VIR',
        'IVB': 'VGB',
        'JCI': 'JEY',
        'KSA': 'SAU',
        'KUW': 'KWT',
        'LAT': 'LVA',
        'LBA': 'LBY',
        'LES': 'LSO',
        'MAD': 'MDG',
        'MAS': 'MYS',
        'MAW': 'MWI',
        'MGL': 'MNG',
        'MNC': 'MCO',
        'MRI': 'MUS',
        'MTN': 'MRT',
        'MYA': 'MMR',
        'NCA': 'NIC',
        'NED': 'NLD',
        'NEP': 'NPL',
        'NGR': 'NGA',
        'OMA': 'OMN',
        'PAR': 'PRY',
        'PHI': 'PHL',
        'PLE': 'PSE',
        'POR': 'PRT',
        'PUR': 'PRI',
        'RSA': 'ZAF',
        'SEY': 'SYC',
        'SLO': 'SVN',
        'SOL': 'SLB',
        'SRI': 'LKA',
        'SUD': 'SDN',
        'SUI': 'CHE',
        'TAN': 'TZA',
        'TOG': 'TGO',
        'UAE': 'ARE',
        'URU': 'URY',
        'VIE': 'VNM',
        'ZAM': 'ZMB',
        'ZIM': 'ZWE',
        'ANT': 'ATG',
        'CAY': 'CYM',
        'IOM': 'IMN',
        'CHA': 'TCD',
        'GEQ': 'GNQ',
        'SKN': 'KNA',
        'VIN': 'VCT',
        'BIZ': 'BLZ',
        'GRN': 'GRD',
        'NIG': 'NER',
        'VAN': 'VUT'}
    
    df['Fed'] = df['Fed'].replace(dict_to_map)
    
    return df
    
###################################################
# Load data into the dataset
###################################################

def update_players_table_sqlalchemy(df, engine):
    """
    Update the 'players' table with new rows from the DataFrame using SQLAlchemy.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data to insert.
        engine: The SQLAlchemy engine connected to the PostgreSQL database.
    """
    # Select relevant columns from the DataFrame
    print("Renaming and selecting relevant columns from the DataFrame...")
    player_data = df[['ID', 'Name', 'Sex', 'B-day']].rename(
        columns={'ID': 'id', 'Name': 'name', 'Sex': 'sex', 'B-day': 'b_day'}
    )

    # Initialize metadata
    print("Initializing metadata and reflecting database schema...")
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Access the 'players' table
    print("Accessing the 'players' table...")
    players_table = Table('players', metadata, autoload_with=engine)

    # Start a session
    with engine.connect() as connection:
        print("Querying existing IDs in the 'players' table...")
        # Query existing IDs in the 'players' table
        existing_ids = connection.execute(select(players_table.c.id)).fetchall()
        #existing_ids = [i[0] for i in existing_ids]
        existing_ids = {row[0] for row in existing_ids}  # Convert to set
        print(f"Converted existing IDs to set...")

        # Filter DataFrame to only include new IDs
        print("Filtering DataFrame to exclude existing IDs...")
        new_rows = player_data[~player_data['id'].isin(existing_ids)]
        print(f"Filtered rows to insert: {len(new_rows)}")

        # Prepare rows to insert
        rows_to_insert = new_rows.to_dict(orient='records')
        print(f"Prepared rows for insertion...")
        
        # Insert new rows into the table
        if rows_to_insert:
            
            try:
                print("Inserting new rows into the 'players' table...")
                with engine.begin() as connection:
                    connection.execute(players_table.insert(), rows_to_insert)
                    print(f"{len(rows_to_insert)} rows added to the 'players' table.")
            except Exception as e:
                print(f"Error inserting rows: {e}")            
        else:
            print("No new rows to add to the 'players' table.")             
            
def update_montlhyupdates_table_sqlalchemy(df, engine):
    """
    Update the 'montlhyupdates' table with new rows or update existing rows from the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data to update or insert.
        engine: The SQLAlchemy engine connected to the PostgreSQL database.
    """
    # Select relevant columns from the DataFrame
    print("Renaming and selecting relevant columns from the DataFrame...")
    month_data = df[['ID', 'Fed', 'Title', 'Number_of_games', 'activity_status', 'Rating', 'Date']].rename(
        columns={
            'ID': 'id',
            'Fed': 'fed',
            'Title': 'title',
            'Number_of_games': 'number_of_games',
            'activity_status': 'activity_status',
            'Rating': 'rating',
            'Date': 'ongoing_date'
        }
    )
    # Initialize metadata
    print("Initializing metadata and reflecting database schema...")
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Access the 'montlhyupdates' table
    print("Accessing the 'montlhyupdates' table...")
    montlhyupdates_table = Table('montlhyupdates', metadata, autoload_with=engine)

    # Start a session
    with engine.connect() as connection:
        # Fetch existing rows based on primary keys
        print("Querying existing primary keys in the 'montlhyupdates' table...")
        existing_rows = connection.execute(
            select(montlhyupdates_table.c.id, montlhyupdates_table.c.ongoing_date)
)           .fetchall()
        existing_keys = {(row[0], row[1]) for row in existing_rows}
        # Split rows into new and existing
        new_rows = month_data[~month_data.apply(
            lambda row: (row['id'], row['ongoing_date']) in existing_keys, axis=1
        )]
        existing_rows = month_data[month_data.apply(
            lambda row: (row['id'], row['ongoing_date']) in existing_keys, axis=1
        )]
        # Insert new rows
        if not new_rows.empty:
            print(f"Prepared rows for insertion...")
            rows_to_insert = new_rows.to_dict(orient='records')            
            try:
                print("Inserting new rows into the 'montlhyupdates' table...")
                with engine.begin() as connection:
                    connection.execute(montlhyupdates_table.insert(), rows_to_insert)
                    print(f"{len(rows_to_insert)} rows added to the 'montlhyupdates' table.")
            except Exception as e:
                print(f"Error inserting rows: {e}")                      
        else:
            print("No new rows to add to the 'montlhyupdates' table.")     
            
###################################################
# Refresh matrialized view
###################################################

# Function to refresh the materialized view
def refresh_materialized_view(view_name, engine):
    """
    Refresh a materialized view in PostgreSQL.

    Parameters:
        view_name (str): The name of the materialized view to refresh.
        engine: The SQLAlchemy engine connected to the PostgreSQL database.
    """
    with engine.connect() as connection:
        # Enable autocommit for non-transactional commands
        connection = connection.execution_options(isolation_level="AUTOCOMMIT")
        try:
            # Refresh the materialized view
            sql = text(f"REFRESH MATERIALIZED VIEW {view_name};")
            connection.execute(sql)
            print(f"Materialized view '{view_name}' refreshed successfully.")
        except Exception as e:
            print(f"Failed to refresh materialized view '{view_name}': {e}")

###################################################
# Move files
###################################################

def move_files(source_path, destination_path, files):
    for file in files:
        source = os.path.join(source_path, file)
        destination = os.path.join(destination_path, file)
        os.rename(source, destination)
        print(f'{file} moved successfully')