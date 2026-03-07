from dash import html, dcc
import dash_bootstrap_components as dbc
from src.constants import (
    DATE_MARKS,
    START_DATE,
    END_DATE,
    DATE_RANGE,
    TIME_MARKS,
    YELLOW_COLOR,
    CHART_COLOR
)
import dash_daq as daq

# Main function to build the dashboard layout
def create_layout():
    return (
        dbc.Container( # Main Bootstrap container
        id="container",
        fluid=True, # fluid layout to adapt to viewport width
        children=[
            dbc.Row(     # Header row: page title and loading spinner
                [dbc.Col(
                    html.H1(
                        "New York Yellow Taxi Trips 2023", # page title
                        className="text-center my-4",      # center text and vertical margin
                        style={"color": "#371418"},        # title text color 
                    ),
                    width=11, # column width 11/12 in Bootstrap grid

                ),
                dbc.Col(   # Loading spinner component to show during callbacks
                    dcc.Loading(
                        id='loading-spinner',
                        overlay_style={"visibility": "visible"},
                        color=CHART_COLOR, # spinner color from constants
                        type="circle",     # spinner style
                        children=[],       # dcc.Loading can wrap children: here left empty (used for the running prop)
                        style={"float": "right", "margin-top":"60%"} # spinner positioning
                    ),
                    width=1 # Narrow column for the spinner (1/12)
                )],
                style={"background-color": YELLOW_COLOR}, # Header row background set to taxi yellow
            ),
            # Main content area: left column with stacked charts, right column with map + toggle
            html.Div(
                [
                    # Left side: two vertically stacked graphs
                    html.Div(
                        [
                            dcc.Graph(
                                id="bar-chart",
                                style={"flex": "1", "height": "auto"},
                                config={"doubleClickDelay": 500,
                                    "modeBarButtonsToRemove": [
                                #"select",
                                "zoom",
                                "lasso2d",
                                "zoomIn2d",
                                "zoomOut2d",
                                "resetScale2d",
                                "toImage",
                                "pan",
                                "autoscale",
                            ], "displaylogo": False},
                            ),  # First graph
                            dcc.Graph(
                                id="hourly-bar-chart", # hourly chart id
                                style={"flex": "1", "height": "auto"},
                                config={"doubleClickDelay": 500,
                                    "modeBarButtonsToRemove": [
                                    # "select",
                                    "zoom",
                                    "lasso2d",
                                    "zoomIn2d",
                                    "zoomOut2d",
                                    "resetScale2d",
                                    "toImage",
                                    "pan",
                                    "autoscale",
                                ], "displaylogo": False},
                            ),  # Second graph (hourly)
                        ],
                        style={
                            "display": "flex",
                            "flex-direction": "column",  # Stack graphs vertically
                            "width": "50%",  # Take half of the container's width
                        },
                    ),
                    # Right side: square nyc-choropleth map and histogram-equalization toggle(avg-distance-graph)
                    html.Div(
                        [
                            # Square nyc-choropleth with button 
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            id="nyc-choropleth",
                                            config={"doubleClickDelay": 500,
                                                    "scrollZoom": True, # allow scroll zoom on the map
                                                    "modeBarButtonsToRemove": [
                                                        "zoom",
                                                        "zoomIn2d",
                                                        "zoomOut2d",
                                                        "resetScale2d",
                                                        "toImage",
                                                    ],
                                                    "displaylogo": False,
                                                    },
                                            style={
                                                "height": "100%",
                                                "width": "90%",
                                                "position": "absolute", # uses absolute positioning inside a relative wrapper to create a square aspect ratio
                                            },
                                        ),
                                        style={
                                            "position": "relative",
                                            "width": "100%",
                                            "padding-bottom": "80%",  # padding-bottom enforces a square aspect ratio (approx square)
                                            "box-sizing": "border-box",
                                            "overflow": "hidden",
                                            "margin": "0 auto",
                                        },
                                    ),
                                    # Button row: row with label and boolean switch for histogram equalization
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.H6(
                                                    "Histogram equalization (10,000 bins):",
                                                    className="mb-2",
                                                    style={"margin-left": "5%"},
                                                ),
                                                width=6,
                                            ),
                                            dbc.Col(
                                                daq.BooleanSwitch(
                                                    id="toggle-heatmap",
                                                    style={"margin-bottom": "0.5em"},
                                                    on=True, # default on
                                                    color=CHART_COLOR
                                                ),
                                                width="auto",
                                            ),
                                        ],
                                        className="g-0", # remove gutters between the columns
                                    ),
                                ],
                                style={
                                    "background-color": "white", # background for map+toggle area
                                },
                            ),
                        ],
                        style={
                            "background-color": "white",
                            "display": "flex",
                            "flex-direction": "column",  # Stack the square graph and avg distance graph vertically
                            "width": "50%",  # Take half of the container's width
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",  # Left and right sides side by side
                    "height": "80vh",  # Make the container take up the full viewport height (80% of the viewport height)
                },
            ),
            # Bottom section: two side-by-side charts (daily trips and average distance)
            html.Div(
                [
                    # Daily trips line chart
                    dcc.Graph(
                        id="daily-trips-graph",
                        style={"width": "50%"},
                        config={
                            "doubleClickDelay": 500,
                            "modeBarButtonsToRemove": [
                                "select",
                                "zoom",
                                "lasso2d",
                                "zoomIn2d",
                                "zoomOut2d",
                                "resetScale2d",
                                "toImage",
                                "pan",
                            ],
                            "displaylogo": False,
                        },
                    ),  
                    # Average trip distance chart
                    dcc.Graph( 
                        id="avg-distance-graph",
                        style={"width": "50%"},
                        config={
                            "doubleClickDelay": 500,
                            "modeBarButtonsToRemove": [
                                "select",
                                "zoom",
                                "lasso2d",
                                "zoomIn2d",
                                "zoomOut2d",
                                "resetScale2d",
                                "toImage",
                            ],
                            "displaylogo": False,
                        },
                    ),  # Adjust width to take half
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",  # Place the graphs side by side (orizontally)
                    "justify-content": "space-between",  # Space the graphs apart
                    "align-items": "flex-start",  # Align graphs at the top
                    "position": "relative",  # Ensure proper stacking context
                },
            ),
        ],
        className="main-container", # top-level class (useful to reference in assets/main.css)
        style={
            "width": "90%",  # internal container width
            "justify-content": "space-between",
            "align-items": "center",
        },
    ))
