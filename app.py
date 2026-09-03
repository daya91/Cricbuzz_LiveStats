import streamlit as st
import requests

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricbuzz LiveStats")
st.subheader("Cricket Analytics Dashboard")

API_KEY = st.secrets["CRICKET_API_KEY"]


@st.cache_data(ttl=60)
def get_matches():
    response = requests.get(
        "https://api.cricapi.com/v1/currentMatches",
        params={
            "apikey": API_KEY,
            "offset": 0
        },
        timeout=15
    )

    response.raise_for_status()

    result = response.json()

    if result.get("status") != "success":
        return []

    return result.get("data", [])


def get_category(match):
    status = match.get("status", "").lower()

    if match.get("matchEnded", False):
        return "Completed"

    if any(word in status for word in [
        "awarded",
        "abandoned",
        "cancelled",
        "canceled",
        "no result"
    ]):
        return "Completed"

    if match.get("matchStarted", False):
        return "Live"

    return "Upcoming"


try:
    matches = get_matches()

    # Dashboard metrics
    live_count = sum(
        get_category(match) == "Live"
        for match in matches
    )

    completed_count = sum(
        get_category(match) == "Completed"
        for match in matches
    )

    upcoming_count = sum(
        get_category(match) == "Upcoming"
        for match in matches
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Live Matches", live_count)

    with col2:
        st.metric("Completed Matches", completed_count)

    with col3:
        st.metric("Upcoming Matches", upcoming_count)

    st.divider()

    # Filter
    st.subheader("🏏 Matches")

    filter_option = st.selectbox(
        "Filter Matches",
        ["All", "Live", "Completed", "Upcoming"]
    )

    filtered_matches = []

    for match in matches:
        category = get_category(match)

        if filter_option == "All" or category == filter_option:
            filtered_matches.append(match)

    st.write(f"Showing **{len(filtered_matches)}** matches")

    # Match cards
    for match in filtered_matches:

        with st.container(border=True):

            st.write(
                f"### {match.get('name', 'Unknown Match')}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(
                    f"**Status:** {match.get('status', 'N/A')}"
                )

            with col2:
                st.write(
                    f"**Type:** {match.get('matchType', 'N/A').upper()}"
                )

            with col3:
                st.write(
                    f"**State:** {get_category(match)}"
                )

            # Score
            scores = match.get("score", [])

            if scores:
                st.write("#### 🏏 Score")

                for score in scores:

                    runs = score.get("r", 0)
                    wickets = score.get("w", 0)
                    overs = score.get("o", 0)
                    inning = score.get(
                        "inning",
                        "Unknown Inning"
                    )

                    st.write(
                        f"**{inning}:** "
                        f"{runs}/{wickets} "
                        f"({overs} overs)"
                    )

            else:
                st.info("Score not available yet.")

except Exception as e:
    st.error(f"Unable to load cricket data: {e}")