import streamlit as st
import pandas as pd
import re
from utils_update_data import add_column_date, clean_df, clean_names, replace_wrongcountry_code_with_right_country_code, check_column, check_country_code

###################################################
# Load txt file into a dataframe
###################################################

# Read the txt file and load it into a dataframe
txt_file_path= 'current_month\standard_mar25frl.txt'
widths = [15, 61, 4, 3, 6, 4, 15, 5, 6, 4, 3, 5, 7]
df = pd.read_fwf(txt_file_path, widths=widths, dtype = {'ID Number':str})
print('The txt file have been loaded into a dataframe')

###################################################
# Data Cleaning
###################################################
# Get only the important columns and rename them
columns = ["ID","Name","Fed","Sex","Title","Number_of_games","B-day","activity_status",'Rating','Year','Month']
rating_column = [item for item in df.columns if re.search(r'\d', item)]
columns_to_get = ['ID Number','Name','Fed','Sex','Tit','Gms','B-day','Flag']
columns_to_get.extend(rating_column)
df = df[columns_to_get]
df = df.rename(columns={"ID Number": "ID", "Tit": "Title","Gms":"Number_of_games","Flag":"activity_status",rating_column[0]:'Rating'})
df_sorted = df.sort_values(['Fed', 'Rating'], ascending=[True, False])
print('The important columns have been selected and renamed')

# Get the top 100 players for each country
top_players = df_sorted.groupby('Fed').head(100)
print('The top 100 strongest players by country have been selected and stored into the "top_players" dataframe')

# Add Column date    
top_players = add_column_date(top_players, rating_column)
print('The column date has been added to "top_players"')

# Data Cleaning
# -> Remove null values from 'ID','Name','Fed','Sex','B-day','Rating'
# -> Fill null values of the column Title with "NT"
# -> Fill null values of the activity_status with "a"
# -> Fill null values of the activity_status with "a"

top_players = clean_df(top_players)
print("Remove null values from 'ID','Name','Fed','Sex','B-day','Rating'")
print('Fill null values of the column Title with "NT"')
print('Fill null values of the activity_status with "a"')
print('Fill null values of the activity_status with "a"')

#Data Cleaning column name
# Extract name part before numbers or parentheses
# Clean trailing spaces and special chars
top_players = clean_names(top_players)
print("Clean players' names")

# Fill the missing values in the B-day column with the median value
top_players.loc[top_players['B-day'].astype('str').str.len() != 4,'B-day']=df['B-day'].median()
print("Fill the missing values in the B-day column with the median value")

# Replace wrong country code with the right country code
top_players = replace_wrongcountry_code_with_right_country_code(top_players)
print('Replace wrong country code with the right country code')

# End message
print('The dataframe contains the top 100 players for each country with the relevant columns')

print("Checking the data...")
# Check the data
# -> ID must be numeric and have a length between 6 and 9
print("ID must be numeric and have a length between 6 and 9")
check_column(top_players, 'ID', is_numeric=True, min_length=6, max_length=9)
# -> Name must not contain numbers
print("Name must not contain numbers")
check_column(top_players, 'Name', contains_no_numbers=True)
# -> Fed must not contain numbers and have a length of 3
print("Fed must not contain numbers and have a length of 3")
check_column(top_players, 'Fed', contains_no_numbers=True, min_length=3, max_length=3)
# Sex must be a single character and not contain numbers
print("Sex must be a single character and not contain numbers")
check_column(top_players, 'Sex', contains_no_numbers=True, min_length=1, max_length=1)
# Title must not contain numbers and have a length between 2 and 3
print("Title must not contain numbers and have a length between 2 and 3")
check_column(top_players, 'Title', contains_no_numbers=True, min_length=2, max_length=3)
# Number_of_games must be numeric and have a length between 1 and 2
print("Number_of_games must be numeric and have a length between 1 and 2")
check_column(top_players, 'Number_of_games', is_numeric=True, min_length=1, max_length=2)
# B-day must be numeric and have a length of 4
print("B-day must be numeric and have a length of 4")
check_column(top_players, 'B-day', is_numeric=True, min_length=4, max_length=4)
# activity_status must not contain numbers and have a length of 1
print("activity_status must not contain numbers and have a length of 1")
check_column(top_players, 'activity_status', contains_no_numbers=True, min_length=1, max_length=1)
# Rating must be numeric and have a length of 4
print("Rating must be numeric and have a length of 4")
check_column(top_players, 'Rating', is_numeric=True, min_length=4, max_length=4)
# Check the country code
check_country_code(top_players)

###################################################
# Data Cleaning
###################################################

print(f'the shape of the dataframe is {top_players.shape}')
top_players['ID'] = top_players['ID'].astype('str')

top_players