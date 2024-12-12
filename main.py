import streamlit as st
from utils import load_data
from utils import customize_title_charts
from utils import customize_plotly_charts
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import plotly.express as px
import os
import re
import plotly.graph_objects as go
import numpy as np
import bar_chart_race as bcr

## App title

st.set_page_config(page_title='Chess Players Analysis :chess_pawn:', layout='wide')
st.title('Chess Players Analytics Dashboard :chess_pawn:')

# Queries

# query = """
#     SELECT 
#     c.country,
#     c.continent,
#     p.date,
#     COUNT(CASE WHEN p.title = 'GM' THEN 1 END) AS count_gm,
#     COUNT(p.title) AS count_title_players,
#     PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY p.rating) AS median_rating
# FROM players p
# LEFT JOIN countries c ON p.fed = c.code    
# WHERE Group_index = 'O'  
#   AND FED not in ('NON','FID') 
#   AND activity_status = 'a' 
# GROUP BY c.country, p.date, c.continent
# ORDER BY p.date ASC, median_rating DESC

# """

# df = load_data(query)

# # Custom color sequence
# custom_color_sequence = ["cornflowerblue", "olivedrab", "maroon", "chocolate", "darkkhaki"]

# # Create the scatter plot
# fig = px.scatter(
#     df,
#     x="count_title_players",
#     y="median_rating",
#     animation_frame="date",
#     animation_group="country",
#     size="count_gm",
#     hover_name="country",
#     color="continent",
#     range_y=[2000, 2700],
#     color_discrete_sequence=custom_color_sequence,
#     width=800,
#     height=400
# )

# # Update the layout to include a title and customize axis fonts
# fig.update_layout(
#     title={
#         'text': "Median Rating vs Amount of Active Titled Players <br> per Country Over Time <br>",
#         'y': 0.94,
#         'x': 0.5,
#         'xanchor': 'center',
#         'yanchor': 'top',
#         'font': dict(size=20)
#     },
#     xaxis=dict(
#         title="Number of Title Players",
#         titlefont=dict(size=14, family="Courier New, monospace"),
#         tickfont=dict(size=12, family="Arial")
#     ),
#     yaxis=dict(
#         title="Median Rating",
#         titlefont=dict(size=14, family="Courier New, monospace"),
#         tickfont=dict(size=12, family="Arial")
#     ),
#     font=dict(family="Courier New, monospace")
# )

# st.plotly_chart(fig,use_container_width=True)

# video_file = open(r"notebooks\download.mp4", "rb")
# video_bytes = video_file.read()

# st.video(video_bytes)


query = f"""
	SELECT
	p.date,
 	round(count (CASE WHEN p.sex = 'M' THEN 1 END)) / (count(*)) AS percentage_men,
	round(count (CASE WHEN p.sex = 'F' THEN 1 END)) / (count(*)) AS percentage_women	
	from players p 
	where p.rating>=1500 and
          extract(month from p.date) = (select get_last_month())
 	group by p.date
	ORDER BY p.date ASC
 	;

"""
df_gender = load_data(query)

# Generate the tick values and labels
#tick_vals = df_gender["date"]
tick_labels = df_gender["date"].dt.strftime("%Y-%m").unique() # Leave as a global variable?

# Create the figure
fig_gender = go.Figure()

# Add the first bar trace (e.g., Men) with custom color
fig_gender.add_trace(go.Bar(
    x=df_gender["date"],
    y=df_gender["percentage_men"].round(2),
    name="Men",
    marker_color="cadetblue"  # Custom color
))
# Add the second bar trace (e.g., Women) with custom color
fig_gender.add_trace(go.Bar(
    x=df_gender["date"],
    y=df_gender["percentage_women"].round(2),
    name="Women",
    marker_color="goldenrod"  # Custom color
))

title_gender = customize_title_charts(text="Trends in Gender Distribution Among Top Players",
                                      y=0.9,
                                      x=0.5,
                                      xanchor='center',
                                      yanchor='top',
                                      font=dict(size=20),
                                      subtitle= dict(
                                        text="Gender percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                                        font=dict(color="gray", size=12))                     
                                        )

fig_gender = customize_plotly_charts(fig=fig_gender,                                     
                                     barmode='stack',
                                     xaxis_title='Date',
                                     yaxis_title='Percentage',
                                     legend_title='Category',
                                     bargap=0.3,
                                     width=800,
                                     height=400,
                                     title=title_gender,
                                     font=dict(
                                        family="Courier New, monospace",
                                        size=12),
                                     tickvals=tick_labels,
                                    ticktext=tick_labels,
                                    tickangle=45                                    
                                    )


st.plotly_chart(fig_gender,use_container_width=True)

















# # Sidebar for Navigation
# page = st.sidebar.selectbox(
#      "Select Dashboard",
#      ("Overview", "Dashboard 1", "Dashboard 2", "Dashboard 3", "Dashboard 4"))

# Example: Fetch top players from the "Open" group

query = """
    SELECT name, rating 
    FROM project.players 
    WHERE Group_index = 'O' AND date = '01-11-2024' AND  activity_status = 'a'
    ORDER BY Rating DESC
    LIMIT 10;
"""
df = load_data(query)
print(df.head())



# Load the selected dashboard
# if page == "Dashboard 1":
#     dashboard_1.show()
# elif page == "Dashboard 2":
#     dashboard_2.show()
# elif page == "Dashboard 3":
#     dashboard_3.show()
# elif page == "Dashboard 4":
#     dashboard_4.show()
# else:
#     st.write("Welcome to the Chess Analytics App! Select a dashboard from the sidebar.")