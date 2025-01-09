import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from utils import get_continent_query_for_bubble_chart
from utils import get_continent_query_for_choropleth
from utils import bubble_chart
from utils import choropleth_map

st.set_page_config(layout="wide")
# Title and subtitle
st.title("Continent Analysis :world_map:")
st.subheader("Discover Metrics, Trends, and Insights from the World of Chess")

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

tab1, tab2, tab3, tab4, tab5 =st.tabs(['Africa 	:earth_africa:', 'Americas 	:earth_americas:', 'Asia 	:earth_asia:', 'Europe	:european_castle:', 'Oceania :desert_island:'])

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