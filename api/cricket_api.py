import requests
import streamlit as st


BASE_URL = "https://api.cricapi.com/v1"


def get_current_matches():
    """Fetch current cricket matches from Cricbuzz API."""

    api_key = st.secrets["CRICKET_API_KEY"]

    url = f"{BASE_URL}/currentMatches"

    params = {
        "apikey": api_key,
        "offset": 0,
    }

    response = requests.get(url, params=params, timeout=15)

    response.raise_for_status()

    return response.json()