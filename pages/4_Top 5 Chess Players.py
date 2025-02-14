import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from utils_pages import load_data
from utils_pages import variation_rating_player_line_chart
from utils_pages import variation_games_played_line_chart
from utils_pages import get_avg_rating_player_current_year
from utils_pages import get_avg_games_played_monthly

st.set_page_config(layout="wide")
# Title and subtitle
st.title("Current Top 5 Chess Players 	:crown:")

query = """
SELECT name,
    rating,
    fed
FROM top_10_open_players_view topv
LIMIT 5
"""
top_5 = [1,2,3,4,5]
container_1 = st.container(border=True)
container_2 = st.container(border=True
                           )
with container_1:
    col1_c1, col2_c1, col3_c1 = st.columns([2,1,1])

    with col1_c1:
        if "df" not in st.session_state:
            st.session_state.df = load_data(query)
            st.session_state.df['Top 5']= top_5
            st.session_state.df.set_index('Top 5',inplace=True)
        event = st.dataframe(
            st.session_state.df,
            #hide_index=True,
            key="data",
            on_select="rerun",
            selection_mode='single-row',
        )
        player = event.selection.rows      

if len(player) > 0:
    
    player[0] +=1    
    player_selected = st.session_state.df['name'].loc[player].values    
    player_selected = player_selected[0]
    
    avg_rating_metric = get_avg_rating_player_current_year(player_selected=player_selected)['avg'].values[0]
    avg_rating_metric = round(avg_rating_metric,2)
    
    avg_games_played = get_avg_games_played_monthly(player_selected=player_selected)['avg'].values[0]
    avg_games_played = round(avg_games_played,2)
    
    col2_c1.metric(label="Ongoing Year's Average Rating", value= avg_rating_metric)
    col3_c1.metric(label= "Monthly Average of Games Played", value=avg_games_played)
    
    fig_player_rating =  variation_rating_player_line_chart(player_selected=player_selected,
                                     text=f" Rating Variations of {player_selected} ",
                                      subtitle=dict(text="Tracking the Professional Chess Rating <br> over the last 10 years <br>",
                                                      font=dict(color="gray", size=12)))

    fig_games = variation_games_played_line_chart(player_selected=player_selected,
                                                text=f'Annual Number of Games Played by {player_selected}',
                                              subtitle=dict(text="Yearly Game Count <br> over the last 10 years <br>",
                                                      font=dict(color="gray", size=12))
                                              )    
    with container_2:
        
        col1_c2, col2_c2 = st.columns([1,1])
        with col1_c2:
            st.plotly_chart(fig_player_rating, use_container_width=True)
        
        with col2_c2:       
            st.plotly_chart(fig_games, use_container_width=True)        

else:
     col2_c1.markdown("No player selected.")
# Add current year games played so far

expander_video = st.expander(label='Bar Chart Race video - Top 5 Chess Players Over Time', icon='📊')
expander_video.video(data = r'top_5_chess_players_over_time.mp4')
