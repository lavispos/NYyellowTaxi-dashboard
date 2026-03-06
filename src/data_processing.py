import polars as pl
from src.constants import PARQUET_FILE


# Load data


def load_data():
    # Read and preprocess the Parquet file
    df = pl.read_parquet(
        PARQUET_FILE,
        columns=[
            "PU_DO_idx",
            "pickup_weekday",
            "tpep_pickup_datetime",
            "trip_distance",
            "DO_borough",
            "DO_zone",
            "PU_zone",
            "time_diff",
            # "speed",
            "PULocationID",
            "DOLocationID",
        ],
        low_memory=True,
    )

    # Ensure column types and extract relevant parts
    df = df.with_columns(
        pl.col("pickup_weekday").cast(pl.datatypes.UInt8),
        pl.col("trip_distance").cast(pl.datatypes.Float32),
        pl.col("tpep_pickup_datetime")
        .cast(pl.Datetime("ms"))
        .alias("tpep_pickup_datetime"),
        pl.col("tpep_pickup_datetime")
        .dt.hour()
        .alias("extracted_hour"),  # Extract the hour
        pl.col("tpep_pickup_datetime")
        .cast(pl.Date)
        .alias("pickup_date"),  # Extract the date
    )

    return df

    # df = df.cast({
    #         "PU_DO_idx": pl.datatypes.UInt32,
    #         "pickup_weekday": pl.datatypes.UInt8,
    #         "tpep_pickup_datetime": pl.datatypes.Datetime("ms"),
    #         "trip_distance": pl.datatypes.Float32,
    #         "pickup_hour": pl.datatypes.UInt8,
    #         "time_diff": pl.datatypes.Float32,
    #         #"speed": pl.datatypes.Float32,
    #     })
    #
    # df = df.with_columns(
    #     pl.col("tpep_pickup_datetime").cast(pl.Date).alias("pickup_date"),  # Extract date
    #     pl.col("tpep_pickup_datetime").dt.hour().alias("extracted_hour")  # Extract hour
    # ).sort("pickup_date")
    #
    # return df


def filter_data(df, start_date, end_date, selected_days, selected_hours):
    filtered_df = df.lazy()

    if (start_date is not None) and (end_date is not None):
        filtered_df = filtered_df.filter(
            (pl.col("tpep_pickup_datetime") >= start_date)
            & (pl.col("tpep_pickup_datetime") <= end_date)
        )

    if selected_days is not None:
        filtered_df = filtered_df.filter(pl.col("pickup_weekday").is_in(selected_days))

    if selected_hours is not None:
        filtered_df = filtered_df.filter(pl.col("extracted_hour").is_in(selected_hours))

    filtered_df = filtered_df.collect()

    return filtered_df


def unique_names(names):
    name_count = {}
    result = []

    for name in names:
        if name not in name_count:
            name_count[name] = 1
            result.append(name)
        else:
            name_count[name] += 1
            unique_name = f"{name} {name_count[name]}"
            result.append(unique_name)

    return result