import streamlit as st
from utils import load_data
from utils import customize_title_charts
from utils import customize_plotly_charts
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(layout="wide")
# Title and subtitle
st.title("Outlook :chess_pawn:")
st.subheader("Discover Metrics, Trends, and Insights from the World of Chess")

st.sidebar.title('Filters')

option_map = {
    'F': "Women",
    'M': 'Men'
    }
#st.sidebar.header("Gender")
st.sidebar.markdown("""
<style>
#gender-header {
    margin-bottom: -100px; /* Adjust the negative value to reduce space */
}
</style>
<h3 id="gender-header">Gender</h3>
""", unsafe_allow_html=True)
 
selected_sex=st.sidebar.multiselect(label="Gender",
                          options=option_map.keys(),
                          format_func= lambda option:option_map[option], 
                          #selection_mode="multi",
                          default=option_map.keys(),
                          label_visibility="hidden")
#st.sidebar.markdown( f"Your selected option: {None if pill_sex is None else [option_map[value] for value in pill_sex]} ")

option_map_1 = {
    'i': "inactive",
    'a': 'active'
    }
#st.sidebar.header("Gender")
st.sidebar.markdown("""
<style>
#activity_status-header {
    margin-bottom: -100px; /* Adjust the negative value to reduce space */
}
</style>
<h3 id="activity_Status-header">Activity Status</h3>
""", unsafe_allow_html=True)
 
selected_activity_Status=st.sidebar.multiselect(label="Activity Status",
                          options=option_map_1.keys(),
                          format_func= lambda option:option_map_1[option], 
                          #selection_mode="multi",
                          default=option_map_1.keys(),
                          label_visibility="hidden")



# Base query components
with_clause = """
WITH pre_aggregations AS (
    SELECT 
        muomv.ongoing_date,
        COUNT(*) AS total_players,
        COUNT(CASE WHEN sex = 'M' THEN 1 END) AS total_men,
        COUNT(CASE WHEN sex = 'F' THEN 1 END) AS total_women,
        COUNT(CASE WHEN c.continent = 'Asia' THEN 1 END) AS total_Asia,
        COUNT(CASE WHEN c.continent = 'Oceania' THEN 1 END) AS total_Oceania,
        COUNT(CASE WHEN c.continent = 'Africa' THEN 1 END) AS total_Africa,
        COUNT(CASE WHEN c.continent = 'Europe' THEN 1 END) AS total_Europe,
        COUNT(CASE WHEN c.continent = 'Americas' THEN 1 END) AS total_Americas,  
        COUNT(CASE WHEN muomv.title IN ('CM','FM','IM','WCM','WFM','WGM','WH','WIM')  THEN 1 END)  AS total_other_titles,
        COUNT(CASE WHEN muomv.title = 'GM' THEN 1 END)  AS total_GMs,
        COUNT(CASE WHEN muomv.title = 'NT' THEN 1 END)  AS total_NO_TITLE,    
        COUNT(CASE WHEN muomv.activity_status = 'a' THEN 1 END)  AS total_active_players,
        COUNT(CASE WHEN muomv.activity_status = 'i' THEN 1 END) AS total_inactive_players,    
        COUNT(CASE WHEN muomv.age_category = 'Less than 19' THEN 1 END)  AS total_less_than_19,
        COUNT(CASE WHEN muomv.age_category = '19-30' THEN 1 END) AS total_19_to_30,
        COUNT(CASE WHEN muomv.age_category = '31-40' THEN 1 END) AS total_31_to_40,
        COUNT(CASE WHEN muomv.age_category = '41-50' THEN 1 END) AS total_41_to_50,
        COUNT(CASE WHEN muomv.age_category = '51-65' THEN 1 END) AS total_51_to_65,
        COUNT(CASE WHEN muomv.age_category = 'More than 66' THEN 1 END)  AS total_more_than_66
    FROM   montlhyupdate_open_players_with_age_group_mv muomv
    LEFT JOIN players p ON muomv.ID = p.ID
    LEFT JOIN countries c ON muomv.fed = c.code
"""
filters = ["EXTRACT(MONTH FROM muomv.ongoing_date) = (SELECT get_last_month())"]

# # Add dynamic filters
# if selected_continent:
#     filters.append("c.continent = %s")
#     params.append(selected_continent)

# if min_rating:
#     filters.append("muomv.rating >= %s")
#     params.append(min_rating)

# if max_rating:
#     filters.append("muomv.rating <= %s")
#     params.append(max_rating)

if selected_sex:
    
    if len(selected_sex) > 1:
    
        filters.append(f"sex in {tuple(selected_sex)}")
        
    else:
        filters.append(f"sex in ('{selected_sex[0]}')")

if selected_activity_Status:
    
    if len(selected_activity_Status) > 1:
    
        filters.append(f"activity_status in {tuple(selected_activity_Status)}")
        
    else:
        filters.append(f"activity_status in ('{selected_activity_Status[0]}')")
    

# Add the WHERE clause if there are filters
if filters:
    with_clause += " WHERE " + " AND ".join(filters)

with_clause += """
GROUP BY ongoing_date
)
"""

# Final SELECT statement
query = with_clause + """
SELECT
    ongoing_date AS date,
    ROUND(total_men * 1.0 / NULLIF(total_players, 0), 2) AS percentage_men,
    ROUND(total_women * 1.0 / NULLIF(total_players, 0), 2) AS percentage_women,
    ROUND(total_Asia  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Asia,
    ROUND(total_Oceania  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Oceania,
    ROUND(total_Africa  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Africa,
    ROUND(total_Europe * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Europe,
    ROUND(total_Americas * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Americas,  
    ROUND(total_other_titles * 1.0 / NULLIF(total_players, 0), 2) AS percentage_other_titles,
    ROUND(total_GMs * 1.0 / NULLIF(total_players, 0), 2) AS percentage_GMs,
    ROUND(total_NO_TITLE * 1.0 / NULLIF(total_players, 0), 2) AS percentage_NO_TITLE,    
    ROUND(total_active_players * 1.0 / NULLIF(total_players, 0), 2) AS percentage_active_players,
    ROUND(total_inactive_players * 1.0 / NULLIF(total_players, 0), 2) AS percentage_inactive_players,    
    ROUND(total_less_than_19 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_less_than_19,
    ROUND(total_19_to_30 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_19_to_30,
    ROUND(total_31_to_40 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_31_to_40,
    ROUND(total_41_to_50 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_41_to_50,
    ROUND(total_51_to_65 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_51_to_65,
    ROUND(total_more_than_66 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_more_than_66
FROM pre_aggregations
ORDER BY ongoing_date ASC
"""
st.write(query)

df = load_data(query)

# Generate the tick values and labels
tick_vals = df["date"]
tick_labels = df["date"].dt.strftime("%Y-%m")

# Create the figure
fig_sex = go.Figure()

# Add the first bar trace (e.g., Men) with custom color
fig_sex.add_trace(go.Bar(
    x=df["date"],
    y=df["percentage_men"].round(2),
    name="Men",
    marker_color="cadetblue"  # Custom color
))

# Add the second bar trace (e.g., Women) with custom color
fig_sex.add_trace(go.Bar(
    x=df["date"],
    y=df["percentage_women"].round(2),
    name="Women",
    marker_color="goldenrod"  # Custom color
))

# Customize the layout
fig_sex.update_layout(
    barmode='stack',  # Options: 'group', 'stack', 'overlay'
    xaxis_title="Date",
    yaxis_title="Percentage",
    legend_title="Category",
    bargap=0.3,  # Adjust spacing between bars (lower = closer)
    width=800,
    height=400,
    title={
        'text': "Trends in Gender Distribution Among Top Players",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font':dict(size=20),
        'subtitle':dict(
                text="Gender percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                font=dict(color="gray", size=12))
        },
    font=dict(
        family="Courier New, monospace",
        size=12)
)

# Update x-axis to display custom tick labels
fig_sex.update_xaxes(
    tickvals=tick_vals,
    ticktext=tick_labels,
    tickangle=45  # Rotate labels for better readability
)


# Example: Ensure your 'date' column is in the correct format
df["date"] = pd.to_datetime(df["date"])

# Generate the tick values and labels
tick_vals = df["date"]
tick_labels = df["date"].dt.strftime("%Y-%m")

# Create the figure
fig_status_activity = go.Figure()

# Add the first bar trace (e.g., Men)
fig_status_activity.add_trace(go.Bar(x=df["date"],
                     y=df["percentage_active_players"].round(2),
                     name="active_players",
                     marker_color='steelblue'))

# Add the second bar trace (e.g., Women)
fig_status_activity.add_trace(go.Bar(x=df["date"],
                     y=df["percentage_inactive_players"].round(2),
                     name="inactive_players",
                     marker_color='rosybrown'))

# Customize the layout
fig_status_activity.update_layout(
    barmode='stack',  # Options: 'group', 'stack', 'overlay'
    xaxis_title="Date",
    yaxis_title="Percentage",
    legend_title="Category",
    width=800,
    height=400,
    title={
        'text': "Percentage of activity status of players Over Time",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font':dict(size=20),
        'subtitle':dict(
                 text="activity status percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                font=dict(color="gray", size=12))
        },
    font=dict(
        family="Courier New, monospace",
        size=12)
)
# Update x-axis to display custom tick labels
fig_status_activity.update_xaxes(
    tickvals=tick_vals,
    ticktext=tick_labels,
    tickangle=45  # Rotate labels for better readability
)




col1, col2 = st.columns(2)

with col1:
    
    st.plotly_chart(fig_sex,use_container_width=True)

with col2:
    st.plotly_chart(fig_status_activity,use_container_width=True)