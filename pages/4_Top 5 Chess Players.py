import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from utils import load_data


st.set_page_config(layout="wide")
# Title and subtitle
st.title("Top 5 Chess Players 	:crown:")

st.video(data = r'notebooks\download.mp4')


query = """
SELECT name,
    rating,
    fed
FROM top_10_open_players_view topv
LIMIT 5
"""

df = load_data(query)

def callable():
    with st.sidebar:
        st.write("**Callback called**")
        st.write(df.loc[st.session_state.df['selection']['rows']])

x = st.dataframe(df, hide_index=True, on_select = callable, selection_mode='single-row', key= 'df')


