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
    return 0
    
    # EZ Method (revenue * 0.3315%)
    if method == "EZ" and revenue <= 2083333:  # $2.083M threshold
        return max(0, revenue * config["tx_rates"]["franchise_ez"])
    
    # Full calculation (68% total revenue OR margin)
    margin_68 = revenue * 0.68
    margin_assets = assets
    margin_payroll = payroll
    
    margin = max(margin_68, margin_assets
    margin, margin_assets, margin_payroll)
    
    tax_due = margin * config["tx_rates"]["franchise_full"]
    return round(max(0, tax_due), 2)

# Sidebar Auth
def sidebar_auth():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("User", key="username")
    password = st.sidebar.text_input("Password", type="password
    if st.sidebar.button("Login"):
        if authenticator.login(username, password):
            st.sidebar.success("✅ Logged in")
            st.session_state.authenticated = True
        else:
            st.sidebar.error("❌ Invalid")
    
    return st.session_state.get('authenticated', False)

# Main Pages
def main_page():
    config = load_config()
    st.title(f"🧾 {config['title']} - {config['version']}")
    
    col1, col2 = st.columns(
