import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Union
from typing import Optional, Dict
import streamlit as st

def get_connection_url() -> str:
    """
    Retrieve the database connection URL from the configuration file.
    Returns:
        str: The database connection URL.
    """
    from config import test_credentials
    return test_credentials()


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
            df["date"] = pd.to_datetime(df["date"])
            return df
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database connection or query execution failed: {e}")
    

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




