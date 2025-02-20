import os
import re
import pandas as pd
from sqlalchemy import create_engine
from monthly_update.utils_update_data import load_data
from monthly_update.utils_update_data import get_connection_url, add_column_date, check_column, check_country_code, clean_df, clean_names, load_data, move_files, refresh_materialized_view, update_montlhyupdates_table_sqlalchemy, update_players_table_sqlalchemy
from monthly_update.utils_update_data import extract_zip, replace_wrongcountry_code_with_right_country_code
import bar_chart_race as bcr
import warnings
warnings.filterwarnings('ignore')

###################################################
# Set up the variables
###################################################

folder_path = r'C:\Users\oscah\Documents\chess rating analytics project\data\current month'
zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')]
url_database = get_connection_url()
engine = create_engine(url_database)
print(url_database)

###################################################
# Execution
###################################################

if len(zip_files) == 1:    
    extract_zip(zip_files=zip_files, folder_path=folder_path)
    txt_file = zip_files[0][:-3]+'txt'
    txt_file_path = os.path.join(folder_path, txt_file)
    # Read the txt file and load it into a dataframe
    widths = [15, 61, 4, 3, 6, 4, 15, 5, 6, 4, 3, 5, 7]
    df = pd.read_fwf(txt_file_path, widths=widths)
    print('The txt file have been loaded into a dataframe')
    # Get only the important columns and rename them
    columns = ["ID","Name","Fed","Sex","Title","Number_of_games","B-day","activity_status",'Rating','Year','Month']
    rating_column = [item for item in df.columns if re.search(r'\d', item)]
    columns_to_get = ['ID Number','Name','Fed','Sex','Tit','Gms','B-day','Flag']
    columns_to_get.extend(rating_column)
    df = df[columns_to_get]
    df = df.rename(columns={"ID Number": "ID", "Tit": "Title","Gms":"Number_of_games","Flag":"activity_status",rating_column[0]:'Rating'})
    df_sorted = df.sort_values(['Fed', 'Rating'], ascending=[True, False])
    # Get the top 100 players for each country
    top_players = df_sorted.groupby('Fed').head(100)    
    top_players = add_column_date(top_players, rating_column)
    top_players = clean_df(top_players)
    top_players = clean_names(top_players)
    top_players.loc[top_players['B-day'].astype('str').str.len() != 4,'B-day']=df['B-day'].median()
    top_players = replace_wrongcountry_code_with_right_country_code(top_players)
    print('The dataframe contains the top 100 players for each country with the relevant columns')
    check_column(top_players, 'ID', is_numeric=True, min_length=6, max_length=9)
    check_column(top_players, 'Name', contains_no_numbers=True)
    check_column(top_players, 'Fed', contains_no_numbers=True, min_length=3, max_length=3)
    check_column(top_players, 'Sex', contains_no_numbers=True, min_length=1, max_length=1)
    check_column(top_players, 'Title', contains_no_numbers=True, min_length=2, max_length=3)
    check_column(top_players, 'Number_of_games', is_numeric=True, min_length=1, max_length=2)
    check_column(top_players, 'B-day', is_numeric=True, min_length=4, max_length=4)
    check_column(top_players, 'activity_status', contains_no_numbers=True, min_length=1, max_length=3)
    check_column(top_players, 'Rating', is_numeric=True, min_length=4, max_length=4)
    check_country_code(top_players)

elif len(zip_files) == 0:
    print('No zip file found in the folder')  
    
###################################################
# Load data into the database
###################################################

print(f'the shape of the dataframe is {top_players.shape}')
top_players['ID'] = top_players['ID'].astype('str')

###################################################
# Players table
###################################################

query = """
    SELECT distinct id
    FROM players p ;
    """
current_unique_ids = load_data(query)
print(current_unique_ids.head())
current_unique_ids = current_unique_ids['id'].to_list()
id_to_add = top_players[~top_players['ID'].isin(current_unique_ids)]
print(f'The number of rows to add is {id_to_add.shape[0]}')

update_players_table_sqlalchemy(top_players, engine)

###################################################
# montlhyupdates table
###################################################

# Update the 'monthlyupdates' table
update_montlhyupdates_table_sqlalchemy(top_players, engine)

###################################################
# refresh the materialized views
###################################################

refresh_materialized_view("montlhyupdate_open_players_with_age_group_mv", engine)

###################################################
# save files
###################################################

source_path = r'C:\Users\oscah\Documents\chess rating analytics project\data\current month'
destination_path_zip = r"C:\Users\oscah\Documents\chess rating analytics project\data\01 raw data"
destination_path_txt = r"C:\Users\oscah\Documents\chess rating analytics project\data\02 semi raw data txt_files"
zip_files = [f for f in os.listdir(source_path) if f.endswith('.zip')]
txt_files = [f for f in os.listdir(source_path) if f.endswith('.txt')]

move_files(source_path, destination_path_zip, zip_files)
move_files(source_path, destination_path_txt, txt_files)

dataset_date = top_players['Date'].dt.strftime("%Y-%m").unique()[0]
top_players_path = r"C:\Users\oscah\Documents\chess rating analytics project\data\03 csv files\open_" + dataset_date + ".csv"
top_players.to_csv(top_players_path, index= False)

###################################################
# update bar chart race - video
###################################################

query = """SELECT *
        FROM top_10_open_players_over_time_view
       ;        
        """
# df = load_data(engine,query)
df = load_data(query)

df["date"] = pd.to_datetime(df["ongoing_date"])
df.drop(columns=['ongoing_date'],inplace=True)

pivot_df = df.pivot_table(
    index="date", 
    columns="name", 
    values="rating"
)
pivot_df.shape

import bar_chart_race as bcr

# Generate the animation
anim = bcr.bar_chart_race(
    df=pivot_df,
    title='Top 5 Chess Players Over The last 10 Years',
    orientation='h',
    sort='desc',
    n_bars=5,
    steps_per_period=20,
    period_length=500,
    perpendicular_bar_func='median',
    figsize=(5, 3),
    dpi=120,
    bar_size=.7,
    period_label={'x': .4, 'y': .93},
    filter_column_colors=False,
    filename='top_5_chess_players_over_time.mp4' 
)