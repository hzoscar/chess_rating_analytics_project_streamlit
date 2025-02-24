import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from utils_pages import get_continent_query_for_bubble_chart
from utils_pages import get_continent_query_for_choropleth
from utils_pages import bubble_chart
from utils_pages import choropleth_map
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
from utils_pages import get_five_figures
from utils_pages import create_placeholder_for_continent_analysis

st.set_page_config(layout="wide")
# Title and subtitle
st.title("Continent Analysis :world_map:")
st.sidebar.title('Filters')

###################################
# General Filters
###################################

option_map_gender, gender_header, selected_gender = filter_gender()
option_map_activity_status, activity_status_header, selected_activity_Status = filter_activity_status()
option_title, title_header, selected_title = filter_title()
option_age, age_header, selected_age = filter_age_group()

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

container_continent_options = st.container(border=False)

with container_continent_options:
    
    col1, col2, col3 = st.columns([1,3,1])
    # Subheader
    #col2.subheader("Choose a continent to explore:")
    continent_chosen = col2.radio(
        "Select a Continent",
        ('Africa', 'Americas', 'Asia', 'Europe', 'Oceania'),
        #('Africa 	:desert:', 'Americas 	:statue_of_liberty:', 'Asia 	:japanese_castle:', 'Europe :european_castle:', 'Oceania :desert_island:'),
        horizontal=True,
        label_visibility='hidden'
    )

if 'Africa' in continent_chosen:
    
    query_africa_bubble_chart = get_continent_query_for_bubble_chart('Africa')
    fig_bubble_chart_africa = bubble_chart(query_africa_bubble_chart,
                                        color_column='subregion',
                                        text='Africa: Median Rating vs Amount of Gms Players per Country Over Time')

    query_africa_choropleth = get_continent_query_for_choropleth('Africa')
    fig_choropleth_africa = choropleth_map(query_africa_choropleth,
                                        scope='africa',
                                        text="Africa: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>")
    
    container_choropleth = st.container(border=False)
    
    with container_choropleth:
        col1, col2, col3 = st.columns([1,3,1])
        col2.plotly_chart(fig_choropleth_africa,use_container_width=True)    
    
    
    expand_anlysis_part = st.expander("Africa - Interactive Filter Analysis", icon="🕵️‍♂️")

    with expand_anlysis_part:
    
        filters.append(f"continent in ('Africa')")
        min_rating = get_min_rating(continent='Africa')
        max_rating = get_max_rating(continent='Africa')
        rating_header, slider_rating = filter_rating(min_rating, max_rating)
        
        if slider_rating:
        
            filters.append(f"muomv.rating >= {slider_rating[0]} AND muomv.rating <= {slider_rating[1]}")   
        
        main_query = get_main_query(filters=filters)
        query_rating = get_rating_query(filters=filters)

        #st.write(query_rating)
        df = load_data(main_query)
        df_rating = load_data(query_rating)
        #st.write(df_rating.head())

        fig_gender, fig_status_activity, fig_title, fig_age, fig_rating = get_five_figures(df= df,
                                                                                        df_rating= df_rating,
                                                                                            selected_title= selected_title,
                                                                                            option_age= option_age)
        
        create_placeholder_for_continent_analysis(selected_gender = selected_gender,
                                                selected_activity_Status = selected_activity_Status,
                                                selected_title= selected_title,
                                                selected_age = selected_age,
                                                filters = filters,
                                                fig_gender = fig_gender,
                                                fig_status_activity=fig_status_activity,
                                                fig_title = fig_title,
                                                fig_age= fig_age,
                                                fig_rating = fig_rating)            

        
    expand_bubble_part = st.expander("Africa - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="▶️")

    with expand_bubble_part:
    
        st.plotly_chart(fig_bubble_chart_africa,use_container_width=True)
        
elif 'Americas' in continent_chosen:

    query_americas_bubble_chart = get_continent_query_for_bubble_chart('Americas')
    fig_bubble_chart_americas = bubble_chart(query_americas_bubble_chart,
                                        color_column='subregion',
                                        text='Americas: Median Rating vs Amount of Gms Players per Country Over Time')

    query_americas_choropleth = get_continent_query_for_choropleth('Americas')
    fig_choropleth_americas = choropleth_map(query_americas_choropleth,
                                        text="Americas: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>",
                                        center= {'lat': 8.983333, 'lon': -79.516670}) #Panama
    
    container_choropleth = st.container(border=False)
    
    with container_choropleth:
        col1, col2, col3 = st.columns([1,4,1])
        col2.plotly_chart(fig_choropleth_americas, use_container_width=True)
    
    expand_anlysis_part = st.expander("Americas - Interactive Filter Analysis", icon="🕵️‍♂️")

    with expand_anlysis_part:
        
        filters.append(f"continent in ('Americas')")
        min_rating = get_min_rating(continent='Americas')
        max_rating = get_max_rating(continent='Americas')
        rating_header, slider_rating = filter_rating(min_rating, max_rating)
        
        if slider_rating:
        
            filters.append(f"muomv.rating >= {slider_rating[0]} AND muomv.rating <= {slider_rating[1]}")   
        
        main_query = get_main_query(filters=filters)
        query_rating = get_rating_query(filters=filters)

        #st.write(query_rating)
        df = load_data(main_query)
        df_rating = load_data(query_rating)
        #st.write(df_rating.head())

        fig_gender, fig_status_activity, fig_title, fig_age, fig_rating = get_five_figures(df= df,
                                                                                        df_rating= df_rating,
                                                                                            selected_title= selected_title,
                                                                                            option_age= option_age)
        
        create_placeholder_for_continent_analysis(selected_gender = selected_gender,
                                                selected_activity_Status = selected_activity_Status,
                                                selected_title= selected_title,
                                                selected_age = selected_age,
                                                filters = filters,
                                                fig_gender = fig_gender,
                                                fig_status_activity=fig_status_activity,
                                                fig_title = fig_title,
                                                fig_age= fig_age,
                                                fig_rating = fig_rating)    
    
    expand_bubble_part = st.expander("America - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="▶️")

    with expand_bubble_part:
    
        st.plotly_chart(fig_bubble_chart_americas,use_container_width=True)

elif 'Asia' in continent_chosen:
    
    query_asia_bubble_chart = get_continent_query_for_bubble_chart('Asia')
    fig_bubble_chart_asia = bubble_chart(query_asia_bubble_chart,
                                        color_column='subregion',
                                        text='Asia: Median Rating vs Amount of Gms Players per Country Over Time')

    query_asia_choropleth = get_continent_query_for_choropleth('Asia')
    fig_choropleth_asia = choropleth_map(query_asia_choropleth,
                                        text="Asia: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>",
                                        scope='asia')    
    
    container_choropleth = st.container(border=False)
    
    with container_choropleth:
        col1, col2, col3 = st.columns([1,4,1])
        col2.plotly_chart(fig_choropleth_asia, use_container_width=True)
    
    expand_anlysis_part = st.expander("Asia - Interactive Filter Analysis", icon="🕵️‍♂️")

    with expand_anlysis_part:
    
        filters.append(f"continent in ('Asia')")
        min_rating = get_min_rating(continent='Asia')
        max_rating = get_max_rating(continent='Asia')
        rating_header, slider_rating = filter_rating(min_rating, max_rating)
        
        if slider_rating:
        
            filters.append(f"muomv.rating >= {slider_rating[0]} AND muomv.rating <= {slider_rating[1]}")   
        
        main_query = get_main_query(filters=filters)
        query_rating = get_rating_query(filters=filters)

        #st.write(query_rating)
        df = load_data(main_query)
        df_rating = load_data(query_rating)
        #st.write(df_rating.head())

        fig_gender, fig_status_activity, fig_title, fig_age, fig_rating = get_five_figures(df= df,
                                                                                        df_rating= df_rating,
                                                                                            selected_title= selected_title,
                                                                                            option_age= option_age)
        
        create_placeholder_for_continent_analysis(selected_gender = selected_gender,
                                                selected_activity_Status = selected_activity_Status,
                                                selected_title= selected_title,
                                                selected_age = selected_age,
                                                filters = filters,
                                                fig_gender = fig_gender,
                                                fig_status_activity=fig_status_activity,
                                                fig_title = fig_title,
                                                fig_age= fig_age,
                                                fig_rating = fig_rating) 
       
    
    expand_bubble_part = st.expander("Asia - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="▶️")

    with expand_bubble_part:
    
        st.plotly_chart(fig_bubble_chart_asia,use_container_width=True)    
        
elif 'Europe' in continent_chosen:
    
    query_europe_bubble_chart = get_continent_query_for_bubble_chart('Europe')
    fig_bubble_chart_europe = bubble_chart(query_europe_bubble_chart,
                                        color_column='subregion',
                                        text='Europe: Median Rating vs Amount of Gms Players per Country Over Time')
    query_europe_choropleth = get_continent_query_for_choropleth('Europe')
    fig_choropleth_europe = choropleth_map(query_europe_choropleth,
                                        text="Europe: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>",
                                        scope='europe')          

    container_choropleth = st.container(border=False)
    
    with container_choropleth:
        col1, col2, col3 = st.columns([1,4,1])
        col2.plotly_chart(fig_choropleth_europe, use_container_width=True)
    
    expand_anlysis_part = st.expander("Europe - Interactive Filter Analysis", icon="🕵️‍♂️")

    with expand_anlysis_part:
        
        filters.append(f"continent in ('Europe')")
        min_rating = get_min_rating(continent='Europe')
        max_rating = get_max_rating(continent='Europe')
        rating_header, slider_rating = filter_rating(min_rating, max_rating)
        
        if slider_rating:
        
            filters.append(f"muomv.rating >= {slider_rating[0]} AND muomv.rating <= {slider_rating[1]}")   
        
        main_query = get_main_query(filters=filters)
        query_rating = get_rating_query(filters=filters)

        #st.write(query_rating)
        df = load_data(main_query)
        df_rating = load_data(query_rating)
        #st.write(df_rating.head())

        fig_gender, fig_status_activity, fig_title, fig_age, fig_rating = get_five_figures(df= df,
                                                                                        df_rating= df_rating,
                                                                                            selected_title= selected_title,
                                                                                            option_age= option_age)
        
        create_placeholder_for_continent_analysis(selected_gender = selected_gender,
                                                selected_activity_Status = selected_activity_Status,
                                                selected_title= selected_title,
                                                selected_age = selected_age,
                                                filters = filters,
                                                fig_gender = fig_gender,
                                                fig_status_activity=fig_status_activity,
                                                fig_title = fig_title,
                                                fig_age= fig_age,
                                                fig_rating = fig_rating)     
    
    expand_bubble_part = st.expander("Europe - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="▶️")

    with expand_bubble_part:
    
        st.plotly_chart(fig_bubble_chart_europe,use_container_width=True)

elif 'Oceania' in continent_chosen:
    
    query_oceania_bubble_chart = get_continent_query_for_bubble_chart('Oceania')
    fig_bubble_chart_oceania = bubble_chart(query_oceania_bubble_chart,
                                        color_column='subregion',
                                        text='Oceania: Median Rating vs Amount of Gms Players per Country Over Time')
    query_oceania_choropleth = get_continent_query_for_choropleth('Oceania')
    fig_choropleth_oceania = choropleth_map(query_oceania_choropleth,
                                        text="Oceania: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>",
                                       )
                                       # center={'lat': -26.853388, 'lon': 133.275154}) 
    container_choropleth = st.container(border=False)
    
    with container_choropleth:
        col1, col2, col3 = st.columns([1,4,1])
        col2.plotly_chart(fig_choropleth_oceania)
    
    expand_anlysis_part = st.expander("Oceania - Interactive Filter Analysis", icon="🕵️‍♂️")

    with expand_anlysis_part:
        
        filters.append(f"continent in ('Oceania')")
        min_rating = get_min_rating(continent='Oceania')
        max_rating = get_max_rating(continent='Oceania')
        rating_header, slider_rating = filter_rating(min_rating, max_rating)
        
        if slider_rating:
        
            filters.append(f"muomv.rating >= {slider_rating[0]} AND muomv.rating <= {slider_rating[1]}")   
        
        main_query = get_main_query(filters=filters)
        query_rating = get_rating_query(filters=filters)

        #st.write(query_rating)
        df = load_data(main_query)
        df_rating = load_data(query_rating)
        #st.write(df_rating.head())

        fig_gender, fig_status_activity, fig_title, fig_age, fig_rating = get_five_figures(df= df,
                                                                                        df_rating= df_rating,
                                                                                            selected_title= selected_title,
                                                                                            option_age= option_age)
        
        create_placeholder_for_continent_analysis(selected_gender = selected_gender,
                                                selected_activity_Status = selected_activity_Status,
                                                selected_title= selected_title,
                                                selected_age = selected_age,
                                                filters = filters,
                                                fig_gender = fig_gender,
                                                fig_status_activity=fig_status_activity,
                                                fig_title = fig_title,
                                                fig_age= fig_age,
                                                fig_rating = fig_rating)     
    
        
    expand_bubble_part = st.expander("Oceania - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="▶️")

    with expand_bubble_part:
    
        st.plotly_chart(fig_bubble_chart_oceania,use_container_width=True)
    


