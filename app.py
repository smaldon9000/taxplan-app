import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import streamlit_authenticator as stauth
import yaml
import base64

st.set_page_config(
    page_title="🧾 Pragmatic TaxPlan v7.1 | TGHC/GAWR/FlareAI",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Config & Credentials
@st.cache_data
def load_config():
    config = {
        "title": "Pragmatic TaxPlan v7.1",
        "version": "2026-03-23",
        "entities": ["TGHC", "GAWR", "FlareAI"],
        "tax_years": [2020,2021,2022,2023,
        2024,2025],
        "tx_rates": {
            "franchise_ez": 0.003315,
            "franchise_full": 0.0075,
            "no_tax_under": 1250000  # $1.23M → $1.25M 2025
        }
    }
    return config

# Texas Franchise Tax Calculator
def tx_franchise_tax(revenue, assets, payroll, year=2025, method="EZ"):
    """Texas Franchise Tax per TGHC/GAWR/FlareAI docs"""
    if revenue < 1250000:  # No
