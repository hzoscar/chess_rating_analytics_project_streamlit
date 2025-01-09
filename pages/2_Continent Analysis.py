import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from utils import get_continent_query_for_bubble_chart
from utils import get_continent_query_for_choropleth
from utils import bubble_chart
from utils import choropleth_map
from utils import load_data
from utils import get_min_rating
from utils import get_max_rating
from utils import get_main_query
from utils import get_average_of_median_rating_over_time
from utils import get_count_unique_countries
from utils import get_rating_query
from utils import filter_gender
from utils import filter_activity_status
from utils import filter_title
from utils import filter_age_group
from utils import filter_rating
from utils import gender_bar_chart
from utils import activity_status_bar_chart
from utils import continents_line_chart
from utils import title_line_chart
from utils import age_group_heat_map
from utils import rating_violin_chart

st.set_page_config(layout="wide")
# Title and subtitle
st.title("Continent Analysis :world_map:")
st.subheader("Discover Metrics, Trends, and Insights from the World of Chess")

tab1, tab2, tab3, tab4, tab5 =st.tabs(['Africa 	:earth_africa:', 'Americas 	:earth_americas:', 'Asia 	:earth_asia:', 'Europe	:european_castle:', 'Oceania :desert_island:'])

###################################
# Filters
###################################

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

























query_africa_bubble_chart = get_continent_query_for_bubble_chart('Africa')
fig_bubble_chart_africa = bubble_chart(query_africa_bubble_chart,
                                       color_column='subregion',
                                       text='Africa: Median Rating vs Amount of Gms Players per Country Over Time')

query_africa_choropleth = get_continent_query_for_choropleth('Africa')
fig_choropleth_africa = choropleth_map(query_africa_choropleth,
                                       scope='africa',
                                       text="Africa: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>")

query_americas_bubble_chart = get_continent_query_for_bubble_chart('Americas')
fig_bubble_chart_americas = bubble_chart(query_americas_bubble_chart,
                                       color_column='subregion',
                                       text='Americas: Median Rating vs Amount of Gms Players per Country Over Time')

query_americas_choropleth = get_continent_query_for_choropleth('Americas')
fig_choropleth_americas = choropleth_map(query_americas_choropleth,
                                       text="Americas: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>",
                                       center= {'lat': 8.983333, 'lon': -79.516670}) #Panama

query_asia_bubble_chart = get_continent_query_for_bubble_chart('Asia')
fig_bubble_chart_asia = bubble_chart(query_asia_bubble_chart,
                                       color_column='subregion',
                                       text='Asia: Median Rating vs Amount of Gms Players per Country Over Time')

query_asia_choropleth = get_continent_query_for_choropleth('Asia')
fig_choropleth_asia = choropleth_map(query_asia_choropleth,
                                       text="Asia: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>",
                                       scope='asia')

query_europe_bubble_chart = get_continent_query_for_bubble_chart('Europe')
fig_bubble_chart_europe = bubble_chart(query_europe_bubble_chart,
                                       color_column='subregion',
                                       text='Europe: Median Rating vs Amount of Gms Players per Country Over Time')
query_europe_choropleth = get_continent_query_for_choropleth('Europe')
fig_choropleth_europe = choropleth_map(query_europe_choropleth,
                                       text="Europe: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>",
                                       scope='europe') 

query_oceania_bubble_chart = get_continent_query_for_bubble_chart('Oceania')
fig_bubble_chart_oceania = bubble_chart(query_oceania_bubble_chart,
                                       color_column='subregion',
                                       text='Oceania: Median Rating vs Amount of Gms Players per Country Over Time')
query_oceania_choropleth = get_continent_query_for_choropleth('Oceania')
fig_choropleth_oceania = choropleth_map(query_oceania_choropleth,
                                       text="Oceania: Current Month's Median Rating, <br> Featuring the Top 100 Players by Country <br>",
                                       )
                                       # center={'lat': -26.853388, 'lon': 133.275154}) 

with tab1:
    st.plotly_chart(fig_choropleth_africa)
    
    st.divider()
    
    expand = st.expander("Africa - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="🫒")

    with expand:
    
        st.plotly_chart(fig_bubble_chart_africa,use_container_width=True)

with tab2:
    st.plotly_chart(fig_choropleth_americas)
    
    st.divider()
    
    expand = st.expander("America - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="🫒")

    with expand:
    
        st.plotly_chart(fig_bubble_chart_americas,use_container_width=True)

with tab3:
    
    st.plotly_chart(fig_choropleth_asia)
    
    st.divider()
    
    expand = st.expander("Asia - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="🫒")

    with expand:
    
        st.plotly_chart(fig_bubble_chart_asia,use_container_width=True)

with tab4:
    
    st.plotly_chart(fig_choropleth_europe)
    
    st.divider()
    
    expand = st.expander("Europe - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="🫒")

    with expand:
    
        st.plotly_chart(fig_bubble_chart_europe,use_container_width=True)

with tab5:
    
    st.plotly_chart(fig_choropleth_oceania)
    
    st.divider()
    
    expand = st.expander("Oceania - Bubble Chart: Median Rating vs Amount og Gms Players per country over time", icon="🫒")

    with expand:
    
        st.plotly_chart(fig_bubble_chart_oceania,use_container_width=True)

    

st.sidebar.title('Filters')