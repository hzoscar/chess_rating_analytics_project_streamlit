import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from utils_pages import get_list_countries
from utils_pages import get_country_query_for_bubble_chart
from utils_pages import bubble_chart
from utils_pages import get_country_query_for_comparison_tool
from utils_pages import get_rating_query
from utils_pages import filter_gender
from utils_pages import filter_activity_status
from utils_pages import filter_title
from utils_pages import filter_age_group
from utils_pages import filters_for_comparison_tool
from utils_pages import load_data
from utils_pages import gender_bar_chart
from utils_pages import activity_status_bar_chart
from utils_pages import title_line_chart
from utils_pages import age_group_heat_map
from utils_pages import rating_violin_chart_for_comparison_tool
from utils_pages import get_metrics_comparison
from utils_pages import filters_for_metrics_comparison_tool

st.set_page_config(layout="wide")
# Title and subtitle
st.title("Comparison Tool 	:toolbox:")

selectbox_container = st.container(border=True)
bubble_chart_container = st.container(border=True)
metrics_container = st.container()
gender_expander = st.expander(label='Gender', icon='👫')
activity_status_expander = st.expander(label='Activity Status', icon='🚥')
title_expander = st.expander(label='Title', icon='👨‍🎓')
age_expander = st.expander(label='Age', icon='👴')
rating_expander = st.expander(label='Rating', icon='📈')

with selectbox_container:
    col1, col2 = st.columns([1, 1])
    
    with  col1:        
        first_country = st.selectbox('Select the first country', get_list_countries(),index=None, placeholder="Russian Federation" )
        if first_country == None:
            first_country = 'Russian Federation'
    with  col2:        
        second_country = st.selectbox('Select the second country', get_list_countries(),index=None, placeholder="United States of America")
        if second_country == None:
            second_country = 'United States of America'

st.sidebar.title('Filters')

option_map_gender, gender_header, selected_gender = filter_gender()
option_map_activity_status, activity_status_header, selected_activity_Status = filter_activity_status()
option_title, title_header, selected_title = filter_title()
option_age, age_header, selected_age = filter_age_group()

filters_first_country = filters_for_comparison_tool(country=first_country,
                                                    selected_gender=selected_gender,
                                                    selected_activity_Status=selected_activity_Status,
                                                    selected_title=selected_title,
                                                    selected_age=selected_age)

filters_second_country = filters_for_comparison_tool(country=second_country,
                                                    selected_gender=selected_gender,
                                                    selected_activity_Status=selected_activity_Status,
                                                    selected_title=selected_title,
                                                    selected_age=selected_age)

filters_metrics = filters_for_metrics_comparison_tool(country=second_country,
                                                    selected_gender=selected_gender,
                                                    selected_activity_Status=selected_activity_Status,
                                                    selected_title=selected_title,
                                                    selected_age=selected_age)

query_comparison_country_bubble_chart = get_country_query_for_bubble_chart(filters=filters_metrics)
first_query = get_country_query_for_comparison_tool(filters_first_country)
second_query = get_country_query_for_comparison_tool(filters_second_country)
rating_query_first_country = get_rating_query(filters=filters_first_country)
rating_query_second_country = get_rating_query(filters=filters_second_country)

df_first_country = load_data(first_query)
df_second_country = load_data(second_query)
df_rating_first_country = load_data(rating_query_first_country)
df_rating_second_country = load_data(rating_query_second_country)

last_date, first_country_count_titled_players, first_country_median_rating, first_country_count_gms, second_country_count_titled_players, second_country_median_rating, second_country_count_gms = get_metrics_comparison(query=query_comparison_country_bubble_chart, first_country=first_country, second_country=second_country)


fig_bubble_chart_comparison = bubble_chart(query_comparison_country_bubble_chart,
                                        color_column='country',
                                        text= f'Median Rating vs Amount of Gms Players Over Time')

gender_bar_chart_first_country = gender_bar_chart(df =df_first_country,
                                                  text=  f"Trends in Gender Distribution Among Top Players <br>{first_country}<br>",
                                                subtitle= dict(
                                                    text="Gender percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                                                    font=dict(color="gray", size=12))
                                            )

gender_bar_chart_second_country = gender_bar_chart(df =df_second_country,
                                                  text=  f"Trends in Gender Distribution Among Top Players <br>{second_country}<br>",
                                                subtitle= dict(
                                                    text="Gender percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                                                    font=dict(color="gray", size=12))
                                            )

activity_status_bar_chart_first_country = activity_status_bar_chart(df =df_first_country,
                                                                    text= f"Percentage of activity status of players Over Time <br>{first_country}<br>",
                                                                    subtitle=dict(
                                                                        text="activity status percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                                                                        font=dict(color="gray", size=12))
                                                                    )

activity_status_bar_chart_second_country = activity_status_bar_chart(df =df_second_country,
                                                                    text= f"Percentage of activity status of players Over Time <br>{second_country}<br>",
                                                                    subtitle=dict(
                                                                        text="activity status percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                                                                        font=dict(color="gray", size=12))
                                                                    )

title_line_chart_first_country = title_line_chart(df =df_first_country,
                                                  text= f"Percentage of titled players Over Time <br>{first_country}<br>",
                                                  selected_title=selected_title,
                                                  subtitle= dict(
                                                      text="title percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                                                      font=dict(color="gray", size=12))
                                                  )
title_line_chart_second_country = title_line_chart(df =df_second_country,
                                                   text= f"Percentage of titled players Over Time <br>{second_country}<br>",
                                                   selected_title=selected_title,
                                                   subtitle= dict(
                                                       text="title percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                                                       font=dict(color="gray", size=12))
                                                   )
age_group_heat_map_first_country = age_group_heat_map(df=df_first_country,
                                                      values_group_age= list(option_age.values()),
                                                        text=f"Age Group Distribution of Players Over Time <br>{first_country}<br>",
                                                        subtitle= dict(
                                                            text="Age group percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                                                            font=dict(color="gray", size=12))
                                                        )      

age_group_heat_map_second_country = age_group_heat_map(df=df_second_country,
                                                      values_group_age= list(option_age.values()),
                                                        text=f"Age Group Distribution of Players Over Time <br>{second_country}<br>",
                                                        subtitle= dict(
                                                            text="Age group percentages among the strongest 100 players <br> per country over the last 5 years <br>",
                                                            font=dict(color="gray", size=12))
                                                        )   

fig_rating = rating_violin_chart_for_comparison_tool(first_country=first_country,
                                                     second_country=second_country,
                                                    df_first_country= df_rating_first_country,
                                                    df_second_country= df_rating_second_country,
                                                        text="Rating Distribution of Players Over Time",
                                                        subtitle=dict(text="Rating distribution among the strongest 100 players <br> per country over the last 5 years <br>",
                                                        font=dict(color="gray", size=12)))                                                        

with bubble_chart_container:
    st.plotly_chart(fig_bubble_chart_comparison, use_container_width=True)

with metrics_container:
    col1, col2 = st.columns(2, vertical_alignment='center')
            
    with col1:
        container_col1 = st.container(border=True)
        container_col1.header(f'{first_country}')
        container_col1.write('metrics current month')
        
        with container_col1:
            
            col1_nested, col2_nested, col3_nested = st.columns([1, 1, 1])           
        
                
            with col1_nested:
                st.metric(label='Median rating', value=first_country_median_rating)
                        
            with col2_nested:
                st.metric(label='Number of Titled Players', value=first_country_count_titled_players)
            
                            
            with col3_nested:
                st.metric(label='Number of Gms', value=first_country_count_gms)
            
    with col2:        
        container_col2 = st.container(border=True)
        container_col2.header(f'{second_country}')
        container_col2.write('metrics current month')
        
        with container_col2:
            col1_nested, col2_nested, col3_nested = st.columns([1, 1,1])           
                                
            with col1_nested:
                st.metric(label='Median rating', value=second_country_median_rating)
                            
            with col2_nested:
                st.metric(label='Number of Titled Players', value=second_country_count_titled_players)
            
            with col3_nested:
                st.metric(label='Number of Gms', value=second_country_count_gms)

with gender_expander:
    col1, col2 = st.columns([1, 1])
    
    with  col1:
        st.plotly_chart(gender_bar_chart_first_country, use_container_width=True, key=f"plot_gender{1}")
    
    with  col2:
        st.plotly_chart(gender_bar_chart_second_country, use_container_width=True, key=f"plot_gender{2}")

with activity_status_expander:
    col1, col2 = st.columns([1, 1])
    
    with  col1:
        st.plotly_chart(activity_status_bar_chart_first_country, use_container_width=True, key=f"plot_activity_status{1}")
    
    with  col2:
        st.plotly_chart(activity_status_bar_chart_second_country, use_container_width=True, key=f"plot_activity_status{2}")

with title_expander:
    col1, col2 = st.columns([1, 1])
    
    with  col1:
        st.plotly_chart(title_line_chart_first_country, use_container_width=True, key=f"plot_title{1}")
    
    with  col2:
        st.plotly_chart(title_line_chart_second_country, use_container_width=True, key=f"plot_title{2}")
        
with age_expander:
    col1, col2 = st.columns([1, 1])
    
    with  col1:
        st.plotly_chart(age_group_heat_map_first_country, use_container_width=True, key=f"plot_age{1}")
    
    with  col2:
        st.plotly_chart(age_group_heat_map_second_country, use_container_width=True, key=f"plot_age{2}")

with rating_expander:
    st.plotly_chart(fig_rating, use_container_width=True)

