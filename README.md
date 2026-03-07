# NY-yellow-taxi-dashboard

## Data provenance & cleaning
**Source:** NYC TLC trip records (Yellow Taxi) — 2023 monthly files.
**Combined dataset (raw):** monthly files merged into a large single table.  
**Cleaning rules applied:**
- Remove trips with `trip_distance == 0`.
- Remove trips with `trip_distance > 330` miles (clearly erroneous).
- Remove trips recorded before 2023.
- Remove rows with negative fare/tip values.
- Remove rows with missing pickup or drop-off locations.
After wrangling, the resulting dataset contains ≈ **35,795,000** trips.
**Reproducibility:** use `src/preprocess.py` (or the Polars snippet below) to reproduce the filtering and to generate the processed parquet files used by the dashboard.

## Design decisions & limitations
**Visualization approach:** multiple coordinated views to support overview → zoom & filter → detail-on-demand. Main views: hourly & daily bar charts, connected scatter plots for trend, pickup→dropoff matrix, choropleth map by taxi zone. Color palette and layout were chosen to improve legibility and accessibility.

**Limitations & next steps:**
- Some filtering operations can be slow due to expensive aggregations; mitigations: caching, pre-aggregation, down-sampling strategies.
- Potential future work: zone/borough granular filters, weather correlation analysis, performance engineering (Dask/Parquet pre-aggregates) and production deployment.
