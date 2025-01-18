import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from utils import load_data
from utils import variation_rating_player_line_chart
from utils import variation_games_played_line_chart


st.set_page_config(layout="wide")
# Title and subtitle
st.title("Top 5 Chess Players 	:crown:")
st.video(data = r'notebooks\download.mp4')


def select_player():
    player_selected = (df['name'].loc[st.session_state.df['selection']['rows']].values)
    return player_selected

query = """
SELECT name,
    rating,
    fed
FROM top_10_open_players_view topv
LIMIT 5
"""

df = load_data(query)
df_st = st.dataframe(df, hide_index=True, on_select = select_player, selection_mode='single-row', key= 'df')


player_selected = select_player()[0]

fig_player_rating, tick_labels =  variation_rating_player_line_chart(player_selected=player_selected,
                                   text=f'rating variation {player_selected}',
                                    subtitle=dict(text="Gender percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                                                    font=dict(color="gray", size=12)))

st.plotly_chart(fig_player_rating, use_container_width=True)


fig_games = variation_games_played_line_chart(player_selected=player_selected,
                                              text=f'rating variation {player_selected}',
                                            subtitle=dict(text="Gender percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                                                    font=dict(color="gray", size=12)),
                                            tick_labels=tick_labels)


st.plotly_chart(fig_games, use_container_width=True)


# Add current year games played so far
# remove subtitle