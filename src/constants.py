from datetime import date
from itertools import accumulate
import polars as pl
import os

ZONE_GEOJSON_FILE = "assets/NYC Taxi Zones.geojson"
BOROUGH_GEOJSON_FILE = "assets/Borough_Boundaries.geojson"
# PARQUET_FILE = "assets/cleaned_filtered_dataset.parquet"
PARQUET_FILE = "assets/cleaned_filtered_dataset.parquet"


BOROUGHS = ["Bronx", "Brooklyn", "Manhattan", "Staten Island", "Queens"]

# Color configurations
PLOTLY_THEMES = {"light": "plotly", "dark": "plotly_dark"}

THEME_MODE = "light"

DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
CUM_SUM_MONTHS = [0] + list(accumulate(DAYS_IN_MONTH))

# Marks for the date range slider
MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

DATE_MARKS = {CUM_SUM_MONTHS[i]: month for i, month in enumerate(MONTHS)}
DATE_MARKS[364] = "Year end"

TIME_MARKS = {
    0: "12 AM",
    3: "3 AM",
    6: "6 AM",
    9: "9 AM",
    12: "12 PM",
    15: "3 PM",
    18: "6 PM",
    21: "9 PM",
    24: "11:59 PM",
}

# For date picker
START_DATE = date(2023, 1, 1)
END_DATE = date(2023, 12, 31)
DATE_RANGE = (END_DATE - START_DATE).days

# Save dictionary with the locationIDs corresponding to each borough
# Use parent path when running constants.py separately
# current_path = os.getcwd()
# parent = os.path.abspath(os.path.join(current_path, os.pardir))
# file_path = os.path.join(parent, 'relative_information', 'taxi_zone_lookup.csv')
file_path = os.path.join("relative_information", "taxi_zone_lookup.csv")

data = pl.read_csv(file_path)

YELLOW_COLOR = "#E4B044"
CHART_COLOR = "#823404"

# Group data by 'Borough' and collect LocationIDs and zone names into a dictionary, sorted by Borough
# Dictionary format: {Borough: [([LocationIDS,...],[Zone names,...])], ...}
BOROUGH_LOCATIONIDS_DICT = (
    data.group_by("Borough").agg(pl.col("LocationID"), pl.col("Zone"))
).rows_by_key(key="Borough")

b1 = "Manhattan"
b2 = "Brooklyn"
b3 = "Staten Island"
b3_short = "SI"
b4 = "Queens"
b5 = "Bronx"
b6 = "EWR"

BOROUGH_ORDER = [b1, b2, b3_short, b4, b5, b6]

# Sorted by borough (Manhattan, Brooklyn, Staten Island, Queens, Bronx),
# then alphabetically sorted.
# Syntax: ([[idx for manhattan], [idx for brooklyn], ...], [[labels for manhattan],[labels for brooklyn],...])
HEATMAP_ORDERING, HEATMAP_LABELS = zip(
    *[
        BOROUGH_LOCATIONIDS_DICT[b1][0],
        BOROUGH_LOCATIONIDS_DICT[b2][0],
        BOROUGH_LOCATIONIDS_DICT[b3][0],
        BOROUGH_LOCATIONIDS_DICT[b4][0],
        BOROUGH_LOCATIONIDS_DICT[b5][0],
        BOROUGH_LOCATIONIDS_DICT[b6][0],
        # BOROUGH_LOCATIONIDS_DICT["N/A"][0],
        # BOROUGH_LOCATIONIDS_DICT["Unknown"]
    ]
)

# Concatenate lists into a single list
HEATMAP_ORDERING = sum(HEATMAP_ORDERING, [])

# Construct list with borough name for each zone
# HEATMAP_LABELS_BOROUGHS = (  [b1]*len(HEATMAP_LABELS[0])
#                           + [b2]*len(HEATMAP_LABELS[1])
#                           + [b3]*len(HEATMAP_LABELS[2])
#                           + [b4]*len(HEATMAP_LABELS[3])
#                           + [b5]*len(HEATMAP_LABELS[4])
#                           + [b6]*len(HEATMAP_LABELS[5])
#                             )

FIRST_ZONE_IN_EACH_BOROUGH = [
    HEATMAP_LABELS[0][0],
    HEATMAP_LABELS[1][0],
    HEATMAP_LABELS[2][0],
    HEATMAP_LABELS[3][0],
    HEATMAP_LABELS[4][0],
    HEATMAP_LABELS[5][0],
]
MID_POINTS = [
    HEATMAP_LABELS[0][len(HEATMAP_LABELS[0]) // 2],
    HEATMAP_LABELS[1][len(HEATMAP_LABELS[1]) // 2],
    HEATMAP_LABELS[2][len(HEATMAP_LABELS[2]) // 2],
    HEATMAP_LABELS[3][len(HEATMAP_LABELS[3]) // 2],
    HEATMAP_LABELS[4][len(HEATMAP_LABELS[4]) // 2],
    HEATMAP_LABELS[5][len(HEATMAP_LABELS[5]) // 2],
]

# Concatenate lists into a single list
HEATMAP_LABELS = sum(HEATMAP_LABELS, [])

HEATMAP_ORDERING_STR = [str(id) for id in HEATMAP_ORDERING]

HEATMAP_ORDERING_DICT = {val: idx for idx, val in enumerate(HEATMAP_ORDERING)}

# Load GeoJSON file for NYC borough boundaries
# with open(BOROUGH_GEOJSON_FILE) as f:
#     NYC_BOROUGH_GEOJSON = json.load(f)

# with open(ZONE_GEOJSON_FILE) as f:
#     NYC_ZONE_GEOJSON = json.load(f)

# MAP_ATTRIBUTES = {
#         "borough": {
#             "geojson": NYC_BOROUGH_GEOJSON,
#             "column_name": "DO_borough",
#             "geojson_property_name": "properties.boro_name",
#         },
# "zone": {
#     'geojson': NYC_ZONE_GEOJSON,
#     "column_name": "DO_zone",
#     "geojson_property_name": "properties.zone",
# }
# }
