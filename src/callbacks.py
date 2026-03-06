# callbacks.py

import datetime
import numpy as np
import polars as pl
import plotly.graph_objects as go
# import plotly.express as px
from dash import Input, Output, State, callback, ctx, no_update
from src.constants import (
    PLOTLY_THEMES,
    BOROUGHS,
    THEME_MODE,
    START_DATE,
    # END_DATE,
    HEATMAP_ORDERING_STR,
    HEATMAP_ORDERING_DICT,
    HEATMAP_LABELS,
    FIRST_ZONE_IN_EACH_BOROUGH,
    BOROUGH_ORDER,
    MID_POINTS,
    CHART_COLOR,
)
from src.data_processing import filter_data, unique_names
from app import df  # Ensure df is imported from app.py

HEATMAP_LABELS = unique_names(HEATMAP_LABELS)


@callback(
    [
        Output("daily-trips-graph", "figure"),
        Output("avg-distance-graph", "figure"),
        Output("nyc-choropleth", "figure"),
        Output("bar-chart", "figure"),
        Output("hourly-bar-chart", "figure"),
    ],
    [
        Input("daily-trips-graph", "relayoutData"),
        Input("bar-chart", 'selectedData'), # Days selected in the daily bar chart
        Input("hourly-bar-chart", 'selectedData'),
        Input("toggle-heatmap", "on")
    ],
    running=[(Output("loading-spinner", "display"), 'show', 'hide')]
)
def update_graphs(
    selected_dates,
    selected_days,  # Days selected in the bar chart
    selected_hours,  # Hours selected in the hourly bar chart
    heatmap_toggle
):
    triggered_id = ctx.triggered_id

    if (selected_dates is not None) and "xaxis.range[0]" in selected_dates: # Range selected
        start_date_str = selected_dates["xaxis.range[0]"]
        start_date = parse_date(start_date_str)
        # start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S.%f').date()

        end_date_str = selected_dates["xaxis.range[1]"]
        end_date = parse_date(end_date_str)
        # end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S.%f').date()
    else:
        start_date = None
        end_date = None

        selected_dates = None

    if selected_days is not None:
        if selected_days["points"] == []:
            selected_days = None
        else:
            # Selected points: {'points': [{'curveNumber': 0, 'pointNumber': 2, 'pointIndex': 2, 'x': 'Wednesday', 'y': 5582454, 'label': 'Wednesday', 'value': 5582454}]}
            selected_days = [bar["pointIndex"] for bar in selected_days["points"]]  # The pointIndex contains the weekday indexed 0-6 for each bar in the 'points' dictionary entry.

    if selected_hours is not None:
        if selected_hours["points"] == []:
            selected_hours = None
        else:
            selected_hours = [bar["pointIndex"] for bar in selected_hours["points"]]

    # Filter data based on date range, weekdays and time of day
    filtered_df = filter_data(
        df, start_date, end_date, selected_days, selected_hours
    )

    if triggered_id == "toggle-heatmap":
        heatmap_fig = create_heatmap_figure(filtered_df, heatmap_toggle)
        return (
            no_update,
            no_update,
            heatmap_fig,
            no_update,
            no_update,
        )

    daily_trips_fig = create_daily_trips_figure(filtered_df)
    avg_distance_fig = create_avg_distance_figure(filtered_df)
    heatmap_fig = create_heatmap_figure(filtered_df, heatmap_toggle)

    bar_chart_fig = create_bar_chart_figure(filtered_df)
    hourly_bar_chart_fig = create_hourly_bar_chart_figure(filtered_df)

    daily_trips_fig.update_layout(template=PLOTLY_THEMES[THEME_MODE])
    avg_distance_fig.update_layout(template=PLOTLY_THEMES[THEME_MODE])
    bar_chart_fig.update_layout(template=PLOTLY_THEMES[THEME_MODE])
    hourly_bar_chart_fig.update_layout(template=PLOTLY_THEMES[THEME_MODE])
    heatmap_fig.update_layout(template=PLOTLY_THEMES[THEME_MODE])

    # Do not update data for charts when filtering on those charts
    # -> there would be no way to undo the filtering and you cannot keep the selection across re-rendering
    if selected_dates is not None:
        daily_trips_fig = no_update

    if selected_days is not None:
        bar_chart_fig = no_update

    if selected_hours is not None:
        hourly_bar_chart_fig = no_update

    return (
        daily_trips_fig,
        avg_distance_fig,
        heatmap_fig,
        bar_chart_fig,
        hourly_bar_chart_fig,
    )


def parse_date(string: str):
    formats = [
        '%Y-%m-%d %H:%M:%S.%f',  # Full date with microseconds
        '%Y-%m-%d %H:%M:%S',     # Full date without microseconds
        '%Y-%m-%d'               # Date without time
    ]

    for fmt in formats:
        try:
            return datetime.datetime.strptime(string, fmt).date()
        except ValueError:
            continue

    # Raise an error if none of the formats work
    raise ValueError(f"Time data '{string}' does not match any known formats")


def create_daily_trips_figure(filtered_df):
    # daily_trips = (
    #     filtered_df.group_by("pickup_date").len(name="trip_count").sort("pickup_date")
    # )
    #
    filtered_df = filtered_df.with_columns(
        pl.col("pickup_date")
        .dt.strftime("%A")  # Format the date as a weekday name
        .alias("day_of_week")
    )
    daily_trips = (
        filtered_df.group_by(["pickup_date", "day_of_week"])
        .len(name="trip_count")
        .sort("pickup_date")
    )
    overall_avg = daily_trips["trip_count"].mean()
    hover_text = [
        f"Date: {date}<br>Day: {day}<br>Trips: {trips}"
        for date, day, trips in zip(
            daily_trips["pickup_date"],
            daily_trips["day_of_week"],
            daily_trips["trip_count"],
        )
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily_trips["pickup_date"],
            y=daily_trips["trip_count"],
            mode="lines+markers",
            name="Daily Trips",
            marker=dict(size=4),
            line=dict(color=CHART_COLOR, width=2),
            hovertext=hover_text,  # Add custom hover text
            hoverinfo="text",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=daily_trips["pickup_date"],  # Extend the line across all dates
            y=[overall_avg] * len(daily_trips["pickup_date"]),
            mode="lines",
            name="Avg. Trips",
            line=dict(color="black", dash="dash", width=1),
        )
    )
    fig.update_layout(
        title="Daily Number of Trips",
        xaxis_title="Date",
        yaxis_title="Number of Trips",
        #legend=dict(x=0.01, y=0.99),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=80, r=50, t=80, b=50),
    )
    return fig


def create_avg_distance_figure(filtered_df):
    filtered_df = filtered_df.with_columns(
        pl.col("pickup_date")
        .dt.strftime("%A")  # Format the date as a weekday name
        .alias("day_of_week")
    )
    daily_distance_stats = (
        filtered_df.group_by(["pickup_date", "day_of_week"])
        .agg([
            pl.col("trip_distance").mean().alias("avg_trip_distance"),
            pl.col("trip_distance").std().alias("std_trip_distance"),
        ])
        .sort("pickup_date")
    )
    dates = daily_distance_stats["pickup_date"].to_list()
    days_of_week = daily_distance_stats["day_of_week"].to_list()
    avg_distances = daily_distance_stats["avg_trip_distance"].to_list()
    std_devs = daily_distance_stats["std_trip_distance"].to_list()

    # Create the upper and lower bounds for the confidence interval
    upper_bound = [avg + (std if std is not None else 0)  # Replace None with 0
    for avg, std in zip(avg_distances, std_devs)]
    lower_bound = [avg - (std if std is not None else 0)  # Replace None with 0
    for avg, std in zip(avg_distances, std_devs)]


    hover_text = [
        f"Date: {date}<br>Day: {day}<br>Avg Distance: {avg:.2f} miles<br>Std Dev: ±{(std if std is not None else 0.00):.2f} miles"
        for date, day, avg, std in zip(dates, days_of_week, avg_distances, std_devs)
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=daily_distance_stats["avg_trip_distance"],
            mode="lines",
            name="Avg. Trip Distance",
            line=dict(color=CHART_COLOR, width=2),
            hovertext=hover_text,  # Add custom hover text
            hoverinfo="text",
        )
    )
    #Add shaded confidence interval
    fig.add_trace(
        go.Scatter(
            x=dates + dates[::-1],  # x-coordinates for the upper and lower bounds
            y=upper_bound + lower_bound[::-1],  # y-coordinates for the upper and lower bounds
            fill="toself",
            fillcolor="rgba(65, 105, 225, 0.2)",  # Semi-transparent royal blue
            line=dict(color="rgba(255, 255, 255, 0)"),  # No line
            hoverinfo="skip",
            name="Std Dev (±1σ)"
        )
    )
    fig.update_layout(
        title="Daily Average Trip Distance",
        xaxis_title="Date",
        yaxis_title="Miles",
        #legend = dict(x=0.01, y=0.99),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=80, r=80, t=80, b=50)
    )
    return fig

def create_bar_chart_figure(filtered_df):


    # Group by 'day_of_week' and calculate the average number of trips for each day
    avg_trips_by_day = (
        filtered_df.group_by("pickup_weekday")  # This is the correct method for Polars
        .agg(
            pl.count("pickup_date").alias("trip_count")
        )  # Count trips per day of the week
        .sort("pickup_weekday")
    )

    # Correctly map day_of_week to day names using a combination of `pl.when()` and `pl.lit()`
    avg_trips_by_day = avg_trips_by_day.with_columns(
        pl.when(pl.col("pickup_weekday") == 0)
        .then(pl.lit("Monday"))
        .when(pl.col("pickup_weekday") == 1)
        .then(pl.lit("Tuesday"))
        .when(pl.col("pickup_weekday") == 2)
        .then(pl.lit("Wednesday"))
        .when(pl.col("pickup_weekday") == 3)
        .then(pl.lit("Thursday"))
        .when(pl.col("pickup_weekday") == 4)
        .then(pl.lit("Friday"))
        .when(pl.col("pickup_weekday") == 5)
        .then(pl.lit("Saturday"))
        .when(pl.col("pickup_weekday") == 6)
        .then(pl.lit("Sunday"))
        .otherwise(pl.lit("Unknown"))
        .alias("day_name")
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=avg_trips_by_day["day_name"],  # Convert to list for Plotly
            y=avg_trips_by_day[
                "trip_count"
            ],  # Convert to list for Plotly
            name="Average Daily Trips",
            marker=dict(color=CHART_COLOR),
        )
    )

    fig.update_layout(
        title="Trips by Day of the Week",
        xaxis_title="Day of the Week",
        yaxis_title="Number of Trips",
        clickmode='event+select', # Set selection as default interaction.
        dragmode=False,  # Disable other interactions
        margin=dict(l=80, r=50, t=50, b=50)
    )

    return fig


def create_hourly_bar_chart_figure(filtered_df):
    hourly_data = (
        filtered_df.group_by("extracted_hour")  # Use `group_by` instead of `groupby`
        .agg(pl.count().alias("trip_count"))
        .sort("extracted_hour")
    )

    # Convert to pandas for Plotly
    hourly_df = hourly_data.to_pandas()

    # Create the bar chart
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=hourly_df["extracted_hour"],
            y=hourly_df["trip_count"],
            marker_color=CHART_COLOR,
        )
    )

    # Add chart labels and title
    fig.update_layout(
        title="Trips by Hour of Day",
        xaxis_title="Hour of Day",
        yaxis_title="Number of Trips",
        xaxis=dict(tickmode="linear", dtick=1),  # Show all hours on x-axis
        template="plotly_white",
        clickmode='event+select',  # Set selection as default interaction.
        dragmode=False,  # Disable other interactions
        margin=dict(l=80, r=50, t=50, b=50)
    )

    return fig


def create_heatmap_figure(filtered_df, hist_equalization, graph_type="Trips"):
    # print('started creating heatmap')

    column_to_look_for = (
        "trip_count"
        if graph_type == "Trips"
        else "trip_distance" if graph_type == "Average Trip Distance" else "speed"
    )

    df_matrix = filtered_df.lazy().group_by(["PULocationID", "DOLocationID"]).agg(
        pl.col("tpep_pickup_datetime").count().alias("trip_count"),
        # pl.col("trip_distance").mean(),
        # pl.col("speed").mean(),
    ).collect()

    # Create a lazy DataFrame with all zone ids [1,263]
    IDs = pl.DataFrame().lazy().with_columns(
        pl.arange(1, 264).alias('ids')
    ).collect()

    # Create a full grid of all (PULocationID, DOLocationID) combinations with value = 0
    full_grid = (
        IDs.join(IDs, how="cross")
        .with_columns(
            pl.col("ids").alias("PULocationID"),
            pl.col("ids_right").alias("DOLocationID"),
            pl.lit(0).alias("zeros")
        )
        .select(["PULocationID", "DOLocationID", "zeros"])
    )

    # Join the full grid with the original DataFrame
    # Use a left join to keep all combinations and overwrite existing values
    df_matrix = full_grid.lazy().join(df_matrix.lazy(), on=["PULocationID", "DOLocationID"], how="left").select(
        pl.col("PULocationID"),
        pl.col("DOLocationID"),
        pl.coalesce([column_to_look_for, 'zeros']).alias(column_to_look_for)
    ).collect()

    # Layout data in grid and only keep relevant column
    df_matrix = df_matrix.pivot(on='PULocationID', index="DOLocationID", values=column_to_look_for)

    # Reorder columns
    df_matrix = df_matrix.select(["DOLocationID"]+HEATMAP_ORDERING_STR)

    # Reorder rows and exclude DOLocationID column
    df_matrix = (df_matrix.sort(pl.col("DOLocationID").replace_strict(HEATMAP_ORDERING_DICT))
                 ).select(pl.exclude("DOLocationID"))

    if hist_equalization:
        np_data = df_matrix.to_numpy()
        df_matrix_eq = histogram_equalization_with_bins(np_data, bins=10000)

        fig = go.Figure(data=go.Heatmap(
            z=df_matrix_eq,
            x=HEATMAP_LABELS,
            y=HEATMAP_LABELS,
            customdata=df_matrix,
            colorscale='solar',
            colorbar=dict(title="#Trips")
        ))

        fig.update_traces(
            hovertemplate="PU zone: %{x}<br>DO zone: %{y}<br>Number of trips: %{customdata} <extra></extra>"
        )

    else:
        # Create the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=df_matrix,
            x=HEATMAP_LABELS,
            y=HEATMAP_LABELS,
            customdata=df_matrix,
            colorscale='solar',
            colorbar=dict(title="#Trips")
        ))
        fig.update_traces(
            hovertemplate="PU zone: %{x}<br>DO zone: %{y}<br>Number of trips: %{z} <extra></extra>"
        )

    # Set up labels for axes to show hierarchical information
    fig.update_layout(
        title=f"{graph_type} between zones",
        xaxis=dict(
            tickvals=FIRST_ZONE_IN_EACH_BOROUGH,  # Only boundary ticks
            ticktext=[""] * len(FIRST_ZONE_IN_EACH_BOROUGH),  # Hide boundary tick labels
            showticklabels=True,  # Keep boundary ticks visible
        ),
        yaxis=dict(
            tickvals=FIRST_ZONE_IN_EACH_BOROUGH,  # Only boundary ticks
            ticktext=[""] * len(FIRST_ZONE_IN_EACH_BOROUGH),  # Hide boundary tick labels
            showticklabels=True,
            autorange="reversed",
        ),
        dragmode="pan",  # Set initial mode to panning for easy navigation
        hovermode="closest",
        margin=dict(l=50, r=20, t=50, b=50)
    )

    # Add labels at the midpoints using annotations
    for i, label in enumerate(BOROUGH_ORDER):
        # Add label to x-axis
        fig.add_annotation(
            x=MID_POINTS[i],
            y=-0.05,  # Adjust y position to align with x-axis labels
            text=label,
            showarrow=False,
            xref="x",
            yref="paper",
            font=dict(size=11),
        )
        # Add label to y-axis
        fig.add_annotation(
            x=-0.05,  # Adjust x position to align with y-axis labels
            y=(MID_POINTS[i] if i != 5 else 275),  # Place 'EWR' at absolute position, so it does not overlap with Bronx
            text=label,
            showarrow=False,
            xref="paper",
            yref="y",
            font=dict(size=11),
            textangle=-90,  # Rotate the text 90 degrees
        )

    fig.update_xaxes(title_text="Pick up zone", title_standoff = 25)
    fig.update_yaxes(title_text="Drop off zone", title_standoff = 25)

    return fig


def histogram_equalization_with_bins(data, bins):
    """
    Perform histogram equalization on integer data with a specific number of bins.

    Parameters:
        data (ndarray): 2D array of integer values.
        bins (int): Number of bins for equalization.

    Returns:
        ndarray: Equalized data normalized to range [0, 1].
    """
    # Flatten the data for histogram computation
    flat_data = data.flatten()

    # Compute the histogram with specified bins
    hist, bin_edges = np.histogram(flat_data, bins=bins, range=(data.min(), data.max()), density=False)

    # Compute the cumulative distribution function (CDF)
    cdf = np.cumsum(hist)
    cdf_normalized = cdf / cdf[-1]  # Normalize CDF to range [0, 1]

    # Map the data values to the CDF using bin edges
    equalized_data = np.interp(flat_data, bin_edges[:-1], cdf_normalized)

    return equalized_data.reshape(data.shape)
