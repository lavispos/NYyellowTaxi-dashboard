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


def create_layout():
    return (
        dbc.Container(
        id="container",
        fluid=True,
        children=[
            dbc.Row(
                [dbc.Col(
                    html.H1(
                        "New York Yellow Taxi Trips 2023",
                        className="text-center my-4",
                        style={"color": "#371418"},
                    ),
                    width=11,

                ),
                dbc.Col(
                    dcc.Loading(
                        id='loading-spinner',
                        overlay_style={"visibility": "visible"},
                        color=CHART_COLOR,
                        type="circle",
                        children=[],
                        style={"float": "right", "margin-top":"60%"}
                    ),
                    width=1
                )],
                style={"background-color": YELLOW_COLOR},
            ),
            html.Div(
                [
                    # Left side with stacked graphs
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
                                id="hourly-bar-chart",
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
                            ),  # Second graph
                        ],
                        style={
                            "display": "flex",
                            "flex-direction": "column",  # Stack graphs vertically
                            "width": "50%",  # Take half of the container's width
                        },
                    ),
                    # Right side with square nyc-choropleth and avg-distance-graph
                    html.Div(
                        [
                            # Square nyc-choropleth with button
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            id="nyc-choropleth",
                                            config={"doubleClickDelay": 500,
                                                    "scrollZoom": True,
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
                                                "position": "absolute",
                                            },
                                        ),
                                        style={
                                            "position": "relative",
                                            "width": "100%",
                                            "padding-bottom": "80%",  # Enforces a square aspect ratio
                                            "box-sizing": "border-box",
                                            "overflow": "hidden",
                                            "margin": "0 auto",
                                        },
                                    ),
                                    # Button row
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
                                                    on=True,
                                                    color=CHART_COLOR
                                                ),
                                                width="auto",
                                            ),
                                        ],
                                        className="g-0",
                                    ),
                                ],
                                style={
                                    "background-color": "white",
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
                    "height": "80vh",  # Make the container take up the full viewport height
                },
            ),
            html.Div(
                [
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
                    ),  # Adjust width to take half
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
                    "flex-direction": "row",  # Place the graphs side by side
                    "justify-content": "space-between",  # Space the graphs apart
                    "align-items": "flex-start",  # Align graphs at the top
                    "position": "relative",  # Ensure proper stacking context
                },
            ),
        ],
        className="main-container",
        style={
            "width": "90%",
            "justify-content": "space-between",
            "align-items": "center",
        },
    ))
