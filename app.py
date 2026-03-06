# app.py
from dash import Dash
import dash_bootstrap_components as dbc

from src.data_processing import load_data
from src.layouts import create_layout
from src.callbacks import *

# Load saved data
df = load_data()

# Instantiate application
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, 'assets/main.css'])
app.layout = create_layout()

if __name__ == "__main__":
    app.run_server(debug=False)
