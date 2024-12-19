import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Union
from typing import Optional, Dict
import streamlit as st
import time

def get_connection_url() -> str:
    """
    Retrieve the database connection URL from the configuration file.
    Returns:
        str: The database connection URL.
    """
    from config import test_credentials
    return test_credentials()


# def test_connection() -> bool:
#     """
#     Test the connection to the database.
#     Returns:
#         bool: True if the connection is successful, False otherwise.
#     """
#     try:
#         # Create an engine and attempt to connect
#         engine = create_engine(get_connection_url())
#         with engine.connect() as connection:
#             print("Connection successful!")
#             return True
#     except SQLAlchemyError as e:
#         print("Error: Unable to connect to the database")
#         print(f"Details: {e}")
#         return False

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

@st.cache_data
def bubble_chart(query):
    
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
    
    return fig







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
        "font": font if font else {"size": 20, "family": "Arial, sans-serif"},
    }

    if subtitle:
        title["subtitle"] = subtitle

    return title


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

