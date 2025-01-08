import streamlit as st
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")
# Title and subtitle
st.title("Continent Analysis :world_map:")
st.subheader("Discover Metrics, Trends, and Insights from the World of Chess")

st.sidebar.title('Filters')

tab1, tab2, tab3, tab4, tab5 =st.tabs(['Africa 	:earth_africa:', 'Americas 	:earth_americas:', 'Asia 	:earth_asia:', 'Europe	:european_castle:', 'Oceania :desert_island:'])

with tab1:
    st.write('Africa')