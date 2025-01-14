import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from utils import get_list_countries
from utils import get_country_query_for_bubble_chart
from utils import bubble_chart


st.set_page_config(layout="wide")
# Title and subtitle
st.title("Comparison Tool 	:toolbox:")
st.sidebar.title('Filters')



first_container = st.container(border=True)

with first_container:
    
    col1, col2 = st.columns([1, 1])
    
    with  col1:        
        first_country = st.selectbox('Select the first country', get_list_countries(),index=None, placeholder="Select a country..." )
        
    with  col2:        
        second_country = st.selectbox('Select the second country', get_list_countries(),index=None, placeholder="Select a country...")

query_comparison_country_bubble_chart = get_country_query_for_bubble_chart(first_country, second_country)

fig_bubble_chart_comparison = bubble_chart(query_comparison_country_bubble_chart,
                                        color_column='country',
                                        text= f'Median Rating vs Amount of Gms Players of {first_country} and {second_country} Over Time')

st.plotly_chart(fig_bubble_chart_comparison, use_container_width=True)