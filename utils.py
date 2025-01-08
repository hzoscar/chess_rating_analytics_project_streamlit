import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Union
from typing import Optional, Dict
import streamlit as st

###################################################
# Conection database
###################################################

def get_connection_url() -> str:
    """
    Retrieve the database connection URL from the configuration file.
    Returns:
        str: The database connection URL.
    """
    from config import test_credentials
    return test_credentials()

@st.cache_data
def load_data(query: str) -> pd.DataFrame:
    """
    Test the connection to the database, then execute a SQL query and return the results as a pandas DataFrame.
    Args:
        query (str): The SQL query to execute.
    Returns:
        pd.DataFrame: Query results as a DataFrame.
    Raises:
        RuntimeError: If the database connection cannot be established or the query fails.
    """
    try:
        # Create the engine and execute the query
        engine = create_engine(get_connection_url())
        with engine.connect() as conn:
            print("Connection successful!")
            # Execute the query
            df = pd.read_sql_query(query, conn)
            
            if 'date' in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            
            return df
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database connection or query execution failed: {e}")

###################################################
# queries
###################################################   

def get_main_query(filters:list) -> str:
    
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
            COUNT(CASE WHEN muomv.title = 'GM' THEN 1 END)  AS total_GM,
            COUNT(CASE WHEN muomv.title = 'NT' THEN 1 END)  AS total_NT,    
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
        ROUND(total_GM * 1.0 / NULLIF(total_players, 0), 2) AS percentage_GM,
        ROUND(total_NT * 1.0 / NULLIF(total_players, 0), 2) AS percentage_NT,    
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
    return query

def get_rating_query(filters:list) -> str:

    query_rating = """
        SELECT muomv.ongoing_date as date,
    muomv.rating
    FROM montlhyupdate_open_players_with_age_group_mv muomv
    LEFT JOIN players p ON muomv.ID = p.ID
    LEFT JOIN countries c ON muomv.fed = c.code

    """
    query_rating += " WHERE " + " AND ".join(filters)
    
    query_rating += " ORDER BY muomv.ongoing_date ASC"

    return query_rating
###################################################
# mesures
###################################################   
    
def get_min_rating() -> int:
    # Example: Fetch top players from the "Open" group
    query = """
        SELECT  min(Rating)
        FROM MontlhyUpdates mu
        ;
    """
    df = load_data(query)
    min_rating = df['min'].values[0]
    
    return min_rating

def get_max_rating() -> int:
    # Example: Fetch top players from the "Open" group
    query = """
        SELECT  max(Rating)
        FROM MontlhyUpdates mu
        ;
    """
    df = load_data(query)
    max_rating = df['max'].values[0]
    
    return max_rating

def get_average_of_median_rating_over_time(filters:list) -> int:
    
    with_clause = """
    WITH preprocessing as (
        SELECT muomv.ongoing_date as date,
        percentile_cont(0.5) WITHIN GROUP (order by muomv.rating) as median_rating
    FROM montlhyupdate_open_players_with_age_group_mv muomv
    LEFT JOIN players p ON muomv.ID = p.ID
    LEFT JOIN countries c ON muomv.fed = c.code """
    
    with_clause += " WHERE " + " AND ".join(filters)
    with_clause += """
    GROUP BY muomv.ongoing_date
    )
    """ 
    query = with_clause + """
        SELECT 
        ROUND(CAST(AVG(median_rating) AS numeric), 2) AS avg_median_rating
        FROM preprocessing """
        
    df = load_data(query)
    average_of_median_rating_over_time = df['avg_median_rating'].values[0]
    
    return average_of_median_rating_over_time

def get_count_unique_countries(filters:list) -> int:
    query = """
        SELECT
    count(distinct country) as unique_countries
    FROM countries c 
    RIGHT JOIN montlhyupdate_open_players_with_age_group_mv muomv ON c.code = muomv.fed
    LEFT JOIN players p ON muomv.ID = p.ID
    """
    query += " WHERE " + " AND ".join(filters)
    
    df = load_data(query)
    count_unique_countries = df['unique_countries'].values[0]
    
    return count_unique_countries
###################################################
# Charts
###################################################

def customize_title_charts(
    text: str,
    y: float = 0.9,
    x: float = 0.5,
    xanchor: str = "center",
    yanchor: str = "top",
    font: Optional[Dict[str, Union[str, int]]] = None,
    subtitle: Optional[Dict[str, Union[str, int]]] = None,
) -> Dict[str, Union[str, float, Dict]]:
    """
    Customize the title configuration for a Plotly chart.

    Parameters:
        text (str): The main title text.
        y (float): Vertical position of the title (default: 0.9).
        x (float): Horizontal position of the title (default: 0.5).
        xanchor (str): Horizontal anchor point ('center', 'left', 'right').
        yanchor (str): Vertical anchor point ('top', 'middle', 'bottom').
        font (Optional[Dict]): Font configuration for the title (e.g., size, family).
        subtitle (Optional[Dict]): Subtitle configuration (e.g., text, font).

    Returns:
        Dict: A dictionary containing the title configuration.
    """
    # Validate xanchor and yanchor values
    if xanchor not in {"center", "left", "right"}:
        raise ValueError("xanchor must be 'center', 'left', or 'right'")
    if yanchor not in {"top", "middle", "bottom"}:
        raise ValueError("yanchor must be 'top', 'middle', or 'bottom'")

    title = {
        "text": text,
        "y": y,
        "x": x,
        "xanchor": xanchor,
        "yanchor": yanchor,
        "font": font if font else {"size": 20},
    }

    if subtitle:
        title["subtitle"] = subtitle

    return title
        
@st.cache_data
def bubble_chart(
    query: str,  # SQL query to fetch data
    text: str    # Text to customize the chart title
) -> px.scatter:  # Returns a Plotly scatter plot object with animation

    # Fetch data using the query and load it into a DataFrame
    df = load_data(query)

    # Convert the 'date' column to datetime format and then to "YYYY-MM" string format
    df['date'] = df["date"].dt.strftime("%Y-%m")

    # Define a custom color sequence for the chart
    custom_color_sequence = ["cornflowerblue", "olivedrab", "maroon", "chocolate", "darkkhaki"]

    # Create an animated scatter plot using Plotly
    fig = px.scatter(
        df,
        x="count of title players",         # X-axis: count of title players
        y="median of rating",               # Y-axis: median of player ratings
        animation_frame="date",             # Frames for animation are based on 'date'
        animation_group="country",          # Groups animation transitions by 'country'
        size="count of Gm",                 # Size of bubbles corresponds to the count of Grandmasters
        hover_name="country",               # Hover displays the country name
        color="continent",                  # Bubbles are colored based on the continent
        range_y=[2000, 2700],               # Y-axis range
        range_x=[0, 100],                   # X-axis range
        color_discrete_sequence=custom_color_sequence,  # Use the custom color sequence
        width=800,                          # Width of the chart
        height=400                          # Height of the chart
    )

    # Update the chart layout to include a title, using a custom title function
    fig.update_layout(
        title=customize_title_charts(text=text)  # Title is dynamically customized using 'text'
    )
    
    # Return the completed chart
    return fig

def gender_bar_chart(
    df:pd.DataFrame,
    text:str,
    subtitle: dict) -> go.Figure:

    # Generate the tick values and labels
    tick_vals = df["date"]
    tick_labels = df["date"].dt.strftime("%Y-%m")

    # Create the figure
    fig_gender = go.Figure()

    # Add the first bar trace (e.g., Men) with custom color
    fig_gender.add_trace(go.Bar(
        x=df["date"],
        y=df["percentage_men"],
        name="Men",
        marker_color="cadetblue"  # Custom color
    ))

    # Add the second bar trace (e.g., Women) with custom color
    fig_gender.add_trace(go.Bar(
        x=df["date"],
        y=df["percentage_women"],
        name="Women",
        marker_color="goldenrod"  # Custom color
    ))

    # Customize the layout
    fig_gender.update_layout(
        barmode='stack',  # Options: 'group', 'stack', 'overlay'
        xaxis_title="Date",
        yaxis_title="Percentage",
        legend_title="Category",
        bargap=0.3,  # Adjust spacing between bars (lower = closer)
        width=800,
        height=400,
        title=customize_title_charts(
            text=text,
            subtitle=subtitle),
        font=dict(
            family="Courier New, monospace",
            size=12)
        )

    # Update x-axis to display custom tick labels
    fig_gender.update_xaxes(
        tickvals=tick_vals,
        ticktext=tick_labels,
        tickangle=45  # Rotate labels for better readability
    )

    return fig_gender

def activity_status_bar_chart(
    df: pd.DataFrame,
    text: str,
    subtitle: dict)-> go.Figure:
    
    # Generate the tick values and labels
    tick_vals = df["date"]
    tick_labels = df["date"].dt.strftime("%Y-%m")

    # Create the figure
    fig_status_activity = go.Figure()

    # Add the first bar trace (e.g., Men)
    fig_status_activity.add_trace(go.Bar(x=df["date"],
                        y=df["percentage_active_players"].round(2),
                        name="active players",
                        marker_color='steelblue'))

    # Add the second bar trace (e.g., Women)
    fig_status_activity.add_trace(go.Bar(x=df["date"],
                        y=df["percentage_inactive_players"].round(2),
                        name="inactive players",
                        marker_color='rosybrown'))

    # Customize the layout
    fig_status_activity.update_layout(
        barmode='stack',  # Options: 'group', 'stack', 'overlay'
        xaxis_title="Date",
        yaxis_title="Percentage",
        legend_title="Category",
        width=800,
        height=400,
        title= customize_title_charts(
            text=text,
            subtitle=subtitle),       
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
    
    return fig_status_activity

def continents_line_chart(
    df: pd.DataFrame,
    selected_continents: list,
    text: str,
    subtitle: dict)-> go.Figure:

    option_continents = ['Oceania', 'Africa', 'Europe', 'Americas', 'Asia']
    
    # Create a set of columns to exclude based on non-selected continents
    not_selected = {continent.lower() for continent in option_continents if continent not in selected_continents}

    # Filter columns that do not end with any of the `not_selected` values
    columns_to_consider = [col for col in df.columns if not any(col.endswith(ns) for ns in not_selected)]
    
    df = df[columns_to_consider]
    
    # Generate the tick values and labels
    tick_vals = df["date"]
    tick_labels = df["date"].dt.strftime("%Y-%m")

    fig_continents = go.Figure()

    if 'Europe' in selected_continents:
        # Add the first bar trace (e.g., percentage_from_31_to_40)
        fig_continents.add_trace(go.Scatter(x=df["date"],
                                y=df["percentage_europe"],
                                name="Europe",
                                marker_color="cornflowerblue")) # royalblue

    if 'Asia' in selected_continents:
        # Add the first bar trace (e.g., percentage_asia)
        fig_continents.add_trace(go.Scatter(x=df["date"],
                                y=df["percentage_asia"],
                                name="Asia",
                                marker_color="olivedrab")) # mediumaquamarine
        
    if 'Americas' in selected_continents:

        # Add the first bar trace (e.g., percentage_from_41_to_50)
        fig_continents.add_trace(go.Scatter(x=df["date"],
                                y=df["percentage_americas"],
                                name="Americas",
                                marker_color="maroon"))# gold                      #here

    if 'Oceania' in selected_continents:
        # Add the first bar trace (e.g., percentage_from_19_to_30)
        fig_continents.add_trace(go.Scatter(x=df["date"],
                                y=df["percentage_oceania"],
                                name="Oceania",
                                marker_color="chocolate")) #coral
    
    if 'Africa' in selected_continents:

        # Add the first bar trace (e.g., percentage_from_31_to_40)
        fig_continents.add_trace(go.Scatter(x=df["date"],
                                y=df["percentage_africa"],
                                name="Africa",
                                marker_color= "darkkhaki"))

    # Customize the layout
    fig_continents.update_layout(
        
        xaxis_title="Date",
        yaxis_title="Percentage",
        legend_title="Category",
        width=800,
        height=400,
        title= customize_title_charts(
            text=text,
            subtitle=subtitle        ),
        font=dict(
            family="Courier New, monospace",
            size=12)           
    )
    fig_continents.update_xaxes(
        tickvals=tick_vals,
        ticktext=tick_labels,
        tickangle=45  # Rotate labels for better readability
    )

    return fig_continents

def title_line_chart(
    df: pd.DataFrame,
    selected_title: list,
    text: str,
    subtitle: dict)-> go.Figure:

    option_title = ['GM', 'NT', 'other_titles']
    
    # Create a set of columns to exclude based on non-selected title
    not_selected = {option.lower() for option in option_title if option not in selected_title}

    # Filter columns that do not end with any of the `not_selected` values
    columns_to_consider = [col for col in df.columns if not any(col.endswith(ns) for ns in not_selected)]
    
    df = df[columns_to_consider]
    
    # Generate the tick values and labels
    tick_vals = df["date"]
    tick_labels = df["date"].dt.strftime("%Y-%m")

    fig_title = go.Figure()

    if 'GM' in selected_title:
        
        fig_title.add_trace(go.Scatter(x=df["date"],
                                y=df["percentage_gm"],
                                name="Grandmaster",
                                marker_color="tan")) # royalblue

    if 'other_titles' in selected_title:
        
        fig_title.add_trace(go.Scatter(x=df["date"],
                                y=df["percentage_other_titles"],
                                name="Other Titles",
                                marker_color="darkslategrey")) # mediumaquamarine
        
    if 'NT' in selected_title:

        fig_title.add_trace(go.Scatter(x=df["date"],
                                y=df["percentage_nt"],
                                name="No Title",
                                marker_color="sienna"))# gold                    #here

    # Customize the layout
    fig_title.update_layout(
        
        xaxis_title="Date",
        yaxis_title="Percentage",
        legend_title="Category",
        width=800,
        height=400,
        title= customize_title_charts(
            text=text,
            subtitle=subtitle        ),
        font=dict(
            family="Courier New, monospace",
            size=12)           
    )
    fig_title.update_xaxes(
        tickvals=tick_vals,
        ticktext=tick_labels,
        tickangle=45  # Rotate labels for better readability
    )

    return fig_title

def age_group_heat_map(
    df: pd.DataFrame,
    values_group_age: list,
    text: str,
    subtitle: dict)-> go.Figure:

    df["date"] = pd.to_datetime(df["date"])
    df["date"].dt.strftime("%Y-%m")

    z_data = np.array([
        df["percentage_less_than_19"],
        df["percentage_19_to_30"],
        df["percentage_31_to_40"],
        df["percentage_41_to_50"],
        df["percentage_51_to_65"],
        df["percentage_more_than_66"],
    ])

    # Create annotations for each cell in the heatmap
    annotations = []
    for i, row in enumerate(z_data):
        for j, value in enumerate(row):
            annotations.append(
                dict(
                    x=df["date"][j],
                    y=values_group_age[i],                
                    text=f"{value*100:.1f}%",  # Format annotation with percentage
                    showarrow=False,
                    font=dict(size=10, color="white" if value*100 > 28 else "black")  # Dynamic text color
                )
            )

    # Create the annotated heatmap
    fig_title = go.Figure(data=go.Heatmap(
        x=df["date"],
        y=values_group_age,
        z=z_data,
        colorscale="Blues",
        colorbar_title="(%)",
    ))
    fig_title.update_layout(
        
        xaxis_title="Date",
        yaxis_title="Age Categories",
        width=800,
        height=400,
        title= customize_title_charts(
            text=text,
            subtitle=subtitle),
        font=dict(
            family="Courier New, monospace",
            size=12)           
    )

    return fig_title

def rating_violin_chart(df: pd.DataFrame,
    text: str,
    subtitle: dict)-> go.Figure:

    # Example: Ensure your 'date' column is in the correct format
    df["date"] = pd.to_datetime(df["date"])

    # Generate the tick values and labels
    #tick_vals = df["date"]
    tick_labels = df["date"].dt.strftime("%Y-%m").unique()

    fig_rating = go.Figure()

    fig_rating.add_trace(go.Violin(x=df['date'],
                            y=df['rating'],
                            legendgroup='Yes', scalegroup='Yes', name='Yes',
                            side='negative',
                            line_color='darkolivegreen')
                )

    fig_rating.update_traces(meanline_visible=True)
    fig_rating.update_layout(
        
        xaxis_title="Date",
        yaxis_title="Rating",
        width=800,
        height=400,
        title= customize_title_charts(
            text=text,
            subtitle=subtitle),
        font=dict(
            family="Courier New, monospace",
            size=12),
        violingap=0.25,
        violinmode='overlay')

    fig_rating.update_xaxes(
        tickvals=tick_labels,
        ticktext=tick_labels,
        tickangle=45  # Rotate labels for better readability
    )
    
    return fig_rating

###################################################
# Filters
###################################################

def filter_gender():
    option_map_gender = {
    'F': "Women",
    'M': 'Men'
    }
    
    gender_header = st.sidebar.markdown("""
    <style>
    #gender-header {
        margin-bottom: -100px; /* Adjust the negative value to reduce space */
    }
    </style>
    <h3 id="gender-header">Gender</h3>
    """, unsafe_allow_html=True)
    
    selected_gender=st.sidebar.pills(label="Gender",
                            options=option_map_gender.keys(),
                            format_func= lambda option:option_map_gender[option], 
                            selection_mode="multi",
                            default=option_map_gender.keys(),
                            label_visibility="hidden")
    
    return option_map_gender, gender_header, selected_gender

def filter_activity_status():
    
    option_map_activity_status = {
        'i': "inactive",
        'a': 'active'
        }
    
    activity_status_header = st.sidebar.markdown("""
    <style>
    #activity_status-header {
        margin-bottom: -100px; /* Adjust the negative value to reduce space */
    }
    </style>
    <h3 id="activity_status-header">Activity Status</h3>
    """, unsafe_allow_html=True)
    
    selected_activity_Status = st.sidebar.pills(
        label="Activity Status",
        options=option_map_activity_status.keys(),
        format_func= lambda option:option_map_activity_status[option],
        selection_mode="multi",
        default=option_map_activity_status.keys(),
        label_visibility="hidden")
    
    return option_map_activity_status, activity_status_header, selected_activity_Status

def filter_continents():
    
    option_continents = ['Oceania', 'Africa', 'Europe', 'Americas', 'Asia']
    
    continents_header = st.sidebar.markdown("""
    <style>
    #continents-header {
        margin-bottom: -100px; /* Adjust the negative value to reduce space */
    }
    </style>
    <h3 id="continents-header">Continents</h3>
    """, unsafe_allow_html=True)
    
    selected_continents = st.sidebar.pills(
        label="Continents",
        options=option_continents,
        #format_func= lambda option:option_map_activity_status[option], 
        selection_mode="multi",
        default= option_continents,
        label_visibility="hidden")
    
    return option_continents, continents_header, selected_continents

def filter_title():
    option_map_title = {
        'GM': "Grandmaster",
        'NT': 'No Title',
        'other_titles': 'Other Titles'
    }

    title_header = st.sidebar.markdown("""
    <style>
    #title-header {
        margin-bottom: -100px; /* Adjust the negative value to reduce space */
    }
    </style>
    <h3 id="title-header">Title</h3>
    """, unsafe_allow_html=True)
    
    selected_title = st.sidebar.pills(
        label="Title",
        options=option_map_title.keys(),
        format_func= lambda option:option_map_title[option],
        selection_mode="multi",
        default=option_map_title.keys(),
        label_visibility="hidden")
    
    return option_map_title, title_header, selected_title

def filter_age_group():
    
    option_map_age = {
        'Less than 19': "0-18",
        '19-30': '19-30',
        '31-40': '31-40',
        '41-50': '41-50',
        '51-65': '51-65',
        'More than 66': '66+'
    }
    
    age_header = st.sidebar.markdown("""
    <style>
    #age-header {
        margin-bottom: -100px; /* Adjust the negative value to reduce space */
    }
    </style>
    <h3 id="age-header">Age Group</h3>
    """, unsafe_allow_html=True)
    
    selected_age = st.sidebar.segmented_control(
        label="Age Group",
        options=option_map_age.keys(),
        format_func= lambda option:option_map_age[option],
        selection_mode="multi",
        default=option_map_age.keys(),
        label_visibility="hidden")
    
    return option_map_age, age_header, selected_age

def filter_rating(min_rating:int, max_rating:int):
    
    rating_header = st.sidebar.markdown("""
    <style>
    #rating-header {
        margin-bottom: -100px; /* Adjust the negative value to reduce space */
    }
    </style>
    <h3 id="rating-header">Rating (Elo range)</h3>
    """, unsafe_allow_html=True)
    
    slider_rating = st.sidebar.slider(
        label="Rating Range",
        step=100,
        value=[min_rating,max_rating],
        min_value=min_rating,
        max_value=max_rating,
        label_visibility="hidden")
    
    
    return rating_header, slider_rating
    


























def customize_plotly_charts(
    fig: go.Figure,   
    barmode: Optional[str] = None,
    xaxis_title: str = "",
    yaxis_title: str = "",
    legend_title: str = "",
    bargap: Optional[float] = None,
    width: int = 800,
    height: int = 600,
    title: Optional[dict] = None,
    font: Optional[dict] = None,
    tickvals: Optional[np.ndarray] = None,
    ticktext: Optional[np.ndarray] = None,
    tickangle: int = 0,
    **kwargs,
) -> go.Figure:
    """
    Customize the layout of a Plotly figure.

    Parameters:
        fig (go.Figure): The Plotly figure to customize.
        type_fig (Optional[str]): Type of figure ('bar', etc.).
        barmode (Optional[str]): Barmode for bar plots ('group', 'stack', 'overlay').
        xaxis_title (str): Title for the x-axis.
        yaxis_title (str): Title for the y-axis.
        legend_title (str): Title for the legend.
        bargap (Optional[float]): Spacing between bars (for bar plots).
        width (int): Width of the plot.
        height (int): Height of the plot.
        title (Optional[dict]): Title configuration for the plot.
        font (Optional[dict]): Font configuration for the plot.
        tickvals (Optional[np.ndarray]): Custom tick values for the x-axis.
        ticktext (Optional[np.ndarray]): Custom tick text for the x-axis.
        tickangle (int): Angle for rotating x-axis tick labels.
        **kwargs: Additional keyword arguments for layout customization.

    Returns:
        go.Figure: The customized Plotly figure.
    """
    layout_updates = {
        "xaxis_title": xaxis_title,
        "yaxis_title": yaxis_title,
        "legend_title": legend_title,
        "width": width,
        "height": height,
        "title": title,
        "font": font,
        "barmode": barmode,
        "bargap": bargap,
        **kwargs,
    }
    fig.update_layout(**layout_updates)

    # Update x-axis properties
    if tickvals is not None and ticktext is not None:
        fig.update_xaxes(tickvals=tickvals, ticktext=ticktext, tickangle=tickangle)

    return fig




