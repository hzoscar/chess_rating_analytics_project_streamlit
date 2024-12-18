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
import time


# query

    # Fetch top players from the "Open" group
query = """
        SELECT 
        c.country,
        c.continent,
        mu.Ongoing_date AS "date",
        COUNT(CASE WHEN mu.title = 'GM' THEN 1 END) AS "count of Gm",
        COUNT(mu.title) AS "count of title players",
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mu.rating) AS "median of rating"
    FROM MontlhyUpdates mu
    LEFT JOIN countries c ON mu.fed = c.code    
    WHERE Group_index = 'O'  
    AND FED not in ('NON','FID') 
    AND activity_status = 'a' 
    GROUP BY c.country, mu.Ongoing_date, c.continent
    ORDER BY mu.Ongoing_date ASC,"median of rating" DESC

"""
st.set_page_config(layout="wide")

# Title and subtitle
st.title("Global Chess Trends Explorer Project! :chess_pawn:")
st.subheader("Discover Metrics, Trends, and Insights from the World of Chess")

st.markdown(""" Here is a taste of what you'll find here: This interactive bubble plot visualizes the relationship between the median Elo rating
                    and the number of active titled players for different countries **over the last 10 years**. Each bubble
                    represents a country and varies in size according to the number of Grandmasters (GM) in that country.
                    **It's important to mention that the data contains only the top 100 strongest players from each country by rating.** 
                        
                        """)
# Show a spinner during a process
# with st.spinner(text="In progress"):
#     time.sleep(3)
#     st.success("Done")

# Show and update progress bar
bar = st.progress(50)
time.sleep(5)
bar.progress(100)

with st.container(border=True):
    
    df = load_data(query)
    df["date"] = pd.to_datetime(df["date"])
    df['date'] = df["date"].dt.strftime("%Y-%m")

    # Custom color sequence
    custom_color_sequence = ["cornflowerblue", "olivedrab", "maroon", "chocolate", "darkkhaki"]

    # Create the scatter plot
    fig = px.scatter(
        df,
        x="count of title players",
        y="median of rating",
        animation_frame="date",
        animation_group="country",
        size="count of Gm",
        hover_name="country",
        color="continent",
        range_y=[2000, 2700],
        range_x=[0,100],
        color_discrete_sequence=custom_color_sequence,
        width=800,
        height=400
    )

    # Update the layout to include a title and customize axis fonts
    fig.update_layout(
        title={
            'text': "Median Rating vs Amount of Active Titled Players <br> per Country Over Time <br>",
            'y': 0.94,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        xaxis=dict(
            title="Number of Title Players",
            titlefont=dict(size=14, family="Courier New, monospace"),
            tickfont=dict(size=12, family="Arial")
        ),
        yaxis=dict(
            title="Median Rating",
            titlefont=dict(size=14, family="Courier New, monospace"),
            tickfont=dict(size=12, family="Arial")
        ),
        font=dict(family="Courier New, monospace")
    )

    st.plotly_chart(fig,use_container_width=True)
    
# Main content
st.markdown("""
As a **passionate chess player**, I’ve always wondered how well my country performs in chess compared to others. 
When I first learned to play chess over 20 years ago, I often heard about Russia's dominance in the game and 
how countries like the United States and India were emerging as strong contenders.

However, there was no clear way to measure how other countries compared to my own in terms of chess performance. 
This curiosity inspired me to create this project. **My goal was to explore the data and uncover meaningful metrics 
and trends in the world of chess.** I’m excited to share these insights with you through this app!
""")

# Project structure
expand = st.expander("The Project", icon="📝")

with expand:

    st.subheader("The Project")
    st.markdown("""
    Given that the primary goal of this project is **to gain insights into how well countries perform in chess**,
    I decided to **focus on the top 100 strongest players from each country by rating over the last 10 years**.
    
    The project consists of seven pages:
    
    1. **Introduction:** This page provides an overview of the project.
    2. **Outlook:** Offers a high-level view of the data and key insights.
    3. **Continent Analysis:** Examines performance and trends by continent.
    4. **Subregion and Country Analysis:** Dives deeper into subregional and country-level performance.
    5. **Comparison Tool:** Allows comparisons between two countries or regions over a selected period.
    6. **Top 5 Chess Players:** Highlights the top 5 players over time.
    7. **Ask a Question:** A bot that answers custom queries directly from the database.
    """)

# Data section
expand = st.expander("The Data", icon="💠")

with expand:
    st.subheader("The Data")
    st.markdown("""
    The data used in this project is sourced from the [FIDE website](https://ratings.fide.com/download_lists.phtml), 
    which provides monthly updates. I downloaded data spanning **the last 10 years**, resulting in 120 text files containing 
    information on all players registered with FIDE—a significant amount of data!

    Since my primary goal was to gain insights into how well countries perform in chess, I decided to focus on the top 
    100 strongest players from each country.

    After preprocessing the data, I created a PostgreSQL database consisting of three tables:
    """)

    # Table descriptions
    st.markdown("""
    **players:** Contains static player information:
    - `id`: Unique identifier for a player.
    - `name`: Name of the player.
    - `sex`: Gender of the player.
    - `b_day`: Year of birth.

    **countries:** Stores geographic attributes:
    - `code`: Country code.
    - `country`: Name of the country.
    - `subregion`: Subregion the country belongs to.
    - `continent`: Continent the country is part of.

    **monthlyupdates:** Holds dynamic player information that changes monthly:
    - `id`: Unique identifier for a player.
    - `rating`: Standard Elo rating.
    - `activity_status`: Indicates whether a player is active or inactive 
    (inactive if no professional game was played in the past year).
    - `number_of_games`: Number of games played in the current month.
    - `title`: Chess title of the player.
    - `fed`: Federation the player represents.
    - `group_index`: Custom attribute with four values: Open, Women, Junior Open, 
    and Junior Women. (For this project, all queries use `group_index='Open').
    - `ongoing_date`: The date the data was recorded.
    """)



#st.caption("This is a string that explains something above.")
#st.caption("A caption with _italics_ :blue[colors] and emojis :sunglasses:")






















# # Sidebar for Navigation
# page = st.sidebar.selectbox(
#      "Select Dashboard",
#      ("Overview", "Dashboard 1", "Dashboard 2", "Dashboard 3", "Dashboard 4"))

# # Example: Fetch top players from the "Open" group

# query = """
#     SELECT name, rating 
#     FROM project.players 
#     WHERE Group_index = 'O' AND date = '01-11-2024' AND  activity_status = 'a'
#     ORDER BY Rating DESC
#     LIMIT 10;
# """
# df = load_data(query)
# print(df.head())



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