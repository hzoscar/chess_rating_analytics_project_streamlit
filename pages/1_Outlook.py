import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from utils import load_data
from utils import filter_gender
from utils import filter_activity_status
from utils import filter_continents
from utils import filter_title
from utils import gender_bar_chart
from utils import activity_status_bar_chart
from utils import continents_line_chart
from utils import title_line_chart


st.set_page_config(layout="wide")
# Title and subtitle
st.title("Outlook :chess_pawn:")
st.subheader("Discover Metrics, Trends, and Insights from the World of Chess")

st.sidebar.title('Filters')

option_map_gender, gender_header, selected_gender = filter_gender()
option_map_activity_status, activity_status_header, selected_activity_Status = filter_activity_status()
option_continents, activity_status_header, selected_continents = filter_continents()    
option_title, title_header, selected_title = filter_title()

# Base query components
with_clause = """
WITH pre_aggregations AS (
    SELECT 
        muomv.ongoing_date,
        COUNT(*) AS total_players,
        COUNT(CASE WHEN sex = 'M' THEN 1 END) AS total_men,
        COUNT(CASE WHEN sex = 'F' THEN 1 END) AS total_women,
        COUNT(CASE WHEN c.continent = 'Asia' THEN 1 END) AS total_Asia,
        COUNT(CASE WHEN c.continent = 'Oceania' THEN 1 END) AS total_Oceania,
        COUNT(CASE WHEN c.continent = 'Africa' THEN 1 END) AS total_Africa,
        COUNT(CASE WHEN c.continent = 'Europe' THEN 1 END) AS total_Europe,
        COUNT(CASE WHEN c.continent = 'Americas' THEN 1 END) AS total_Americas,  
        COUNT(CASE WHEN muomv.title IN ('CM','FM','IM','WCM','WFM','WGM','WH','WIM')  THEN 1 END)  AS total_other_titles,
        COUNT(CASE WHEN muomv.title = 'GM' THEN 1 END)  AS total_GM,
        COUNT(CASE WHEN muomv.title = 'NT' THEN 1 END)  AS total_NT,    
        COUNT(CASE WHEN muomv.activity_status = 'a' THEN 1 END)  AS total_active_players,
        COUNT(CASE WHEN muomv.activity_status = 'i' THEN 1 END) AS total_inactive_players,    
        COUNT(CASE WHEN muomv.age_category = 'Less than 19' THEN 1 END)  AS total_less_than_19,
        COUNT(CASE WHEN muomv.age_category = '19-30' THEN 1 END) AS total_19_to_30,
        COUNT(CASE WHEN muomv.age_category = '31-40' THEN 1 END) AS total_31_to_40,
        COUNT(CASE WHEN muomv.age_category = '41-50' THEN 1 END) AS total_41_to_50,
        COUNT(CASE WHEN muomv.age_category = '51-65' THEN 1 END) AS total_51_to_65,
        COUNT(CASE WHEN muomv.age_category = 'More than 66' THEN 1 END)  AS total_more_than_66
    FROM   montlhyupdate_open_players_with_age_group_mv muomv
    LEFT JOIN players p ON muomv.ID = p.ID
    LEFT JOIN countries c ON muomv.fed = c.code
"""
filters = ["EXTRACT(MONTH FROM muomv.ongoing_date) = (SELECT get_last_month())"]

if selected_gender:
    
    if len(selected_gender) > 1:
    
        filters.append(f"sex in {tuple(selected_gender)}")
        
    else:
        filters.append(f"sex in ('{selected_gender[0]}')")

if selected_activity_Status:
    
    if len(selected_activity_Status) > 1:
    
        filters.append(f"activity_status in {tuple(selected_activity_Status)}")
        
    else:
        filters.append(f"activity_status in ('{selected_activity_Status[0]}')")

if selected_continents:
    
    if len(selected_continents) > 1:
    
        filters.append(f"continent in {tuple(selected_continents)}")
        
    else:
        filters.append(f"continent in ('{selected_continents[0]}')")
     
other_titles_list = ['CM','FM','IM','WCM','WFM','WGM','WH','WIM'] 
        
if selected_title:
    
    if 'other_titles' in selected_title:
        
        if len(selected_title) == 1:
                
            filters.append(f"title in {tuple(other_titles_list)}")

        else:
            option_to_consider_title = [i for i in selected_title if i != 'other_titles']
            option_to_consider_title.extend(other_titles_list)
            
            filters.append(f"title in {tuple(option_to_consider_title)}")
            
    else:
        
        if len(selected_title) > 1:
    
            filters.append(f"title in {tuple(selected_title)}")
        
        else:
            filters.append(f"title in ('{selected_title[0]}')")        
        

# Add the WHERE clause if there are filters
if filters:
    with_clause += " WHERE " + " AND ".join(filters)

with_clause += """
GROUP BY ongoing_date
)
"""

# Final SELECT statement
query = with_clause + """
SELECT
    ongoing_date AS date,
    ROUND(total_men * 1.0 / NULLIF(total_players, 0), 2) AS percentage_men,
    ROUND(total_women * 1.0 / NULLIF(total_players, 0), 2) AS percentage_women,
    ROUND(total_Asia  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Asia,
    ROUND(total_Oceania  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Oceania,
    ROUND(total_Africa  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Africa,
    ROUND(total_Europe * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Europe,
    ROUND(total_Americas * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Americas,  
    ROUND(total_other_titles * 1.0 / NULLIF(total_players, 0), 2) AS percentage_other_titles,
    ROUND(total_GM * 1.0 / NULLIF(total_players, 0), 2) AS percentage_GM,
    ROUND(total_NT * 1.0 / NULLIF(total_players, 0), 2) AS percentage_NT,    
    ROUND(total_active_players * 1.0 / NULLIF(total_players, 0), 2) AS percentage_active_players,
    ROUND(total_inactive_players * 1.0 / NULLIF(total_players, 0), 2) AS percentage_inactive_players,    
    ROUND(total_less_than_19 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_less_than_19,
    ROUND(total_19_to_30 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_19_to_30,
    ROUND(total_31_to_40 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_31_to_40,
    ROUND(total_41_to_50 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_41_to_50,
    ROUND(total_51_to_65 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_51_to_65,
    ROUND(total_more_than_66 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_more_than_66
FROM pre_aggregations
ORDER BY ongoing_date ASC
"""
#st.write(query)

df = load_data(query)

fig_gender = gender_bar_chart(
    df = df,
    text=  "Trends in Gender Distribution Among Top Players",
    subtitle= dict(
                text="Gender percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                font=dict(color="gray", size=12))
    )


fig_status_activity = activity_status_bar_chart(
    df=df,
    text="Percentage of activity status of players Over Time",
    subtitle=dict(
                 text="activity status percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                font=dict(color="gray", size=12))
    )

fig_continents = continents_line_chart(
    df=df,
    selected_continents=selected_continents,
    text="Participation of Players by Continent Over Time",
    subtitle= dict(
                 text="Percentages of top 100 players per country<br> segmented by continent over the last 10 years <br>",
                font=dict(
                    color="gray",
                    size=12))
            )

fig_title = title_line_chart(
    df=df,
    selected_title=selected_title,
    text="Percentage of title players Over Time",
    subtitle= dict(
                 text="title percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                font=dict(color="gray", size=12))
    )


placeholder = st.container()

with placeholder:
    
    if not(selected_gender) or not(selected_activity_Status) or not(selected_continents) or not(selected_title):
        placeholder.header('Each filter has to have at least one option selected.')
        
        if not(selected_gender):                            
            placeholder.subheader('Filter Gender is empty') 
                
        elif not(selected_activity_Status):                
            placeholder.subheader('Filter Activity Status is empty')
        
        elif not(selected_continents):
            placeholder.subheader('Filter Continents is empty')
        
        elif not(selected_title):
            placeholder.subheader('Filter Title is empty')
            
    else:
            
        col1, col2 = st.columns(2)

        with col1:           
              
            st.plotly_chart(fig_gender,use_container_width=True)
            st.plotly_chart(fig_continents, use_container_width=True)

        with col2:
            
            st.plotly_chart(fig_status_activity,use_container_width=True)
            st.plotly_chart(fig_title, use_container_width=True)
    
   