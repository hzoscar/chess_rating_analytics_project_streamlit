import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from utils_pages import load_data
from utils_pages import get_min_rating
from utils_pages import get_max_rating
from utils_pages import get_main_query
from utils_pages import get_average_of_median_rating_over_time
from utils_pages import get_count_unique_countries
from utils_pages import get_rating_query
from utils_pages import filter_gender
from utils_pages import filter_activity_status
from utils_pages import filter_title
from utils_pages import filter_age_group
from utils_pages import filter_rating
from utils_pages import gender_bar_chart
from utils_pages import activity_status_bar_chart
from utils_pages import continents_line_chart
from utils_pages import title_line_chart
from utils_pages import age_group_heat_map
from utils_pages import rating_violin_chart

st.set_page_config(layout="wide")
# Title and subtitle
st.title("Outlook 	:earth_africa:")
st.subheader("Discover Metrics, Trends, and Insights from the World of Chess")

st.sidebar.title('Filters')

min_rating = get_min_rating()
max_rating = get_max_rating()

option_map_gender, gender_header, selected_gender = filter_gender()
option_map_activity_status, activity_status_header, selected_activity_Status = filter_activity_status()
option_title, title_header, selected_title = filter_title()
option_age, age_header, selected_age = filter_age_group()
rating_header, slider_rating = filter_rating(min_rating, max_rating)

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

if selected_age:
    
    if len(selected_age) > 1:
    
        filters.append(f"age_category in {tuple(selected_age)}")
        
    else:
        filters.append(f"age_category in ('{selected_age[0]}')")     

if slider_rating:
    
    filters.append(f"muomv.rating >= {slider_rating[0]} AND muomv.rating <= {slider_rating[1]}")   

main_query = get_main_query(filters=filters)
query_rating = get_rating_query(filters=filters)

#st.write(query_rating)
df = load_data(main_query)
df_rating = load_data(query_rating)
#st.write(df_rating.head())

fig_gender = gender_bar_chart(
    df = df,
    text=  "Trends in Gender Distribution Among Top Players",
    subtitle= dict(
                text="Gender percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                font=dict(color="gray", size=12))
    )

fig_status_activity = activity_status_bar_chart(
    df=df,
    text="Percentage of activity status of players Over Time",
    subtitle=dict(
                 text="activity status percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                font=dict(color="gray", size=12))
    )

fig_continents = continents_line_chart(
    df=df,    
    text="Participation of Players by Continent Over Time",
    subtitle= dict(
                 text="Percentages of top 100 players per country<br> segmented by continent over the last 5 years <br>",
                font=dict(
                    color="gray",
                    size=12))
            )

fig_title = title_line_chart(
    df=df,
    selected_title=selected_title,
    text="Percentage of titled players Over Time",
    subtitle= dict(
                 text="title percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                font=dict(color="gray", size=12))
    )

fig_age = age_group_heat_map(
    df=df,
    values_group_age= list(option_age.values()),
    text="Age Group Distribution of Players Over Time",
    subtitle= dict(
                 text="Age group percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                font=dict(color="gray", size=12))
    )

fig_rating = rating_violin_chart(
    df=df_rating,
    text="Rating Distribution of Players Over Time",
    subtitle= dict(
                 text="Rating distribution among the strongest 100 players <br> per country over the last 5 years <br>",
                font=dict(color="gray", size=12))
    )

placeholder = st.container()

with placeholder:
    
    if not(selected_gender) or not(selected_activity_Status) or not(selected_title) or not(selected_age): 
        placeholder.header('Each filter has to have at least one option selected.')
        
        if not(selected_gender):                            
            placeholder.subheader('Filter Gender is empty') 
                
        elif not(selected_activity_Status):                
            placeholder.subheader('Filter Activity Status is empty')       
        
        elif not(selected_title):
            placeholder.subheader('Filter Title is empty')
        
        elif not(selected_age):
            placeholder.subheader('Filter Age Group is empty')
            
    else:
            
        col1, col2 = st.columns(2)
        
        with col1:           
            st.markdown(
            f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 0px;  margin: 25px; text-align: center;">
                <h4>Average of median rating over time</h4>
                <p style="font-size: 20px;">{get_average_of_median_rating_over_time(filters=filters)}</p>
            </div>
            """,
            unsafe_allow_html=True)
            st.plotly_chart(fig_gender,use_container_width=True)
            st.plotly_chart(fig_continents, use_container_width=True)
            st.plotly_chart(fig_age, use_container_width=True)

        with col2:
            st.markdown(
            f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 0px; margin: 25px; text-align: center;">
                <h4>Total Countries considered</h4>
                <p style="font-size: 20px;">{get_count_unique_countries(filters=filters)}</p>
            </div>
            """,
            unsafe_allow_html=True)
            st.plotly_chart(fig_status_activity,use_container_width=True)
            st.plotly_chart(fig_title, use_container_width=True)
            st.plotly_chart(fig_rating, use_container_width=True)
