import streamlit as st
import requests

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricbuzz LiveStats")
st.subheader("Cricket Analytics Dashboard")
from services.player_service import get_all_players, create_player, update_player, delete_player
from services.match_service import (
    get_all_matches,
    create_match,
    update_match,
    delete_match,
)
from utils.db_connection import get_connection
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
    st.error("Unable to load cricket data: {e}")
# Player Management
st.divider()
st.header("👤 Player Management")

players = get_all_players()

team_options = {
    "India": 1,
    "Australia": 2,
    "England": 3,
    "South Africa": 4,
    "New Zealand": 5
}

team_id_to_name = {value: key for key, value in team_options.items()}

if players:
    st.subheader("All Players")

    for player in players:
        player_id, player_name, team_id, role, batting_style, bowling_style = player

        with st.container(border=True):
            st.write(f"### {player_name}")
            st.write(f"**Player ID:** {player_id}")
            st.write(
                f"**Team:** {team_id_to_name.get(team_id, f'Team ID {team_id}')}"
            )
            st.write(f"**Role:** {role or 'N/A'}")
            st.write(f"**Batting Style:** {batting_style or 'N/A'}")
            st.write(f"**Bowling Style:** {bowling_style or 'N/A'}")

else:
    st.info("No players found.")


# Edit Player
st.subheader("✏️ Edit Player")

player_ids = [player[0] for player in players]

if player_ids:

    selected_player_id = st.selectbox(
        "Select Player",
        player_ids,
        format_func=lambda player_id: next(
            player[1] for player in players if player[0] == player_id
        )
    )

    selected_player = next(
        player for player in players if player[0] == selected_player_id
    )

    (
        selected_id,
        selected_name,
        selected_team_id,
        selected_role,
        selected_batting_style,
        selected_bowling_style,
    ) = selected_player

    with st.form("edit_player_form"):

        edit_player_name = st.text_input(
            "Player Name",
            value=selected_name
        )

        edit_team_name = st.selectbox(
            "Team",
            list(team_options.keys()),
            index=list(team_options.values()).index(selected_team_id)
        )

        edit_role = st.selectbox(
            "Role",
            ["Batter", "Bowler", "All-rounder", "Wicketkeeper"],
            index=[
                "Batter",
                "Bowler",
                "All-rounder",
                "Wicketkeeper"
            ].index(selected_role)
            if selected_role in [
                "Batter",
                "Bowler",
                "All-rounder",
                "Wicketkeeper"
            ]
            else 0
        )

        edit_batting_style = st.selectbox(
            "Batting Style",
            ["Right-hand", "Left-hand"],
            index=(
                ["Right-hand", "Left-hand"].index(selected_batting_style)
                if selected_batting_style in ["Right-hand", "Left-hand"]
                else 0
            )
        )

        edit_bowling_style = st.text_input(
            "Bowling Style",
            value=selected_bowling_style or ""
        )

        update_submitted = st.form_submit_button("Update Player")

        if update_submitted:

            if not edit_player_name.strip():
                st.error("Player name is required.")

            else:
                try:
                    update_player(
                        selected_id,
                        edit_player_name.strip(),
                        team_options[edit_team_name],
                        edit_role,
                        edit_batting_style,
                        edit_bowling_style.strip() or None
                    )

                    st.success(
                        f"Player '{edit_player_name.strip()}' updated successfully!"
                    )

                    st.rerun()

                except Exception as e:
                    st.error(f"Unable to update player: {e}")

# Delete Player
st.subheader("🗑️ Delete Player")

players = get_all_players()

if players:

    delete_player_options = {
        player[1]: player[0]
        for player in players
    }

    delete_player_name = st.selectbox(
        "Select Player to Delete",
        list(delete_player_options.keys()),
        key="delete_player_select"
    )

    if st.button("🗑️ Delete Player", type="secondary"):

        selected_delete_id = delete_player_options[delete_player_name]

        try:
            deleted = delete_player(selected_delete_id)

            if deleted:
                st.success(
                    f"Player '{delete_player_name}' deleted successfully!"
                )
                st.rerun()
            else:
                st.error("Player not found.")

        except Exception as e:
            st.error(f"Unable to delete player: {e}")
# Create New Player
st.subheader("➕ Create New Player")

with st.form("create_player_form"):

    player_id = st.number_input(
        "Player ID",
        min_value=1,
        step=1
    )

    player_name = st.text_input("Player Name")

    team_name = st.selectbox(
        "Team",
        list(team_options.keys())
    )

    role = st.selectbox(
        "Role",
        ["Batter", "Bowler", "All-rounder", "Wicketkeeper"]
    )

    batting_style = st.selectbox(
        "Batting Style",
        ["Right-hand", "Left-hand"]
    )

    bowling_style = st.text_input(
        "Bowling Style",
        placeholder="Example: Right-arm Fast"
    )

    submitted = st.form_submit_button("Create Player")

    if submitted:

        if not player_name.strip():
            st.error("Player name is required.")

        else:
            try:
                create_player(
                    int(player_id),
                    player_name.strip(),
                    team_options[team_name],
                    role,
                    batting_style,
                    bowling_style.strip() or None
                )

                st.success(
                    f"Player '{player_name.strip()}' created successfully!"
                )

                st.rerun()

            except Exception as e:
                st.error(f"Unable to create player: {e}")
# Match Management
st.divider()
st.header("🏏 Match Management")

matches_db = get_all_matches()

if matches_db:
    st.subheader("All Matches")

    for match in matches_db:
        (
            match_id,
            series_id,
            venue_id,
            team1_id,
            team1_name,
            team2_id,
            team2_name,
            match_type,
            match_date,
            status,
            winner_team_id,
            win_margin,
            victory_type,
        ) = match

        with st.container(border=True):
            st.write(f"### {team1_name} vs {team2_name}")
            st.write(f"**Match ID:** {match_id}")
            st.write(f"**Match Type:** {match_type or 'N/A'}")
            st.write(f"**Date:** {match_date or 'N/A'}")
            st.write(f"**Status:** {status or 'N/A'}")

            if winner_team_id:
                winner_name = (
                    team1_name
                    if winner_team_id == team1_id
                    else team2_name
                )
                st.write(
                    f"**Winner:** {winner_name}"
                )

            if win_margin:
                st.write(
                    f"**Win Margin:** {win_margin} "
                    f"{victory_type or ''}"
                )

else:
    st.info("No matches found.")

# Create Match
st.subheader("➕ Create New Match")

team_options = {
    "India": 1,
    "Australia": 2,
    "England": 3,
    "South Africa": 4,
    "New Zealand": 5,
}

with st.form("create_match_form"):

    match_id = st.number_input(
        "Match ID",
        min_value=1,
        step=1,
    )

    team1_name = st.selectbox(
        "Team 1",
        list(team_options.keys()),
    )

    team2_name = st.selectbox(
        "Team 2",
        list(team_options.keys()),
    )

    match_type = st.selectbox(
        "Match Type",
        ["Test", "ODI", "T20", "T20I"],
    )

    match_date = st.date_input(
        "Match Date",
    )

    status = st.selectbox(
        "Status",
        ["upcoming", "live", "completed"],
    )

    submitted = st.form_submit_button(
        "Create Match"
    )

    if submitted:

        if team1_name == team2_name:
            st.error("Team 1 and Team 2 must be different.")

        else:
            try:
                create_match(
                    int(match_id),
                    None,
                    None,
                    team_options[team1_name],
                    team_options[team2_name],
                    match_type,
                    str(match_date),
                    status,
                    None,
                    None,
                    None,
                )

                st.success(
                    f"Match '{team1_name} vs {team2_name}' "
                    "created successfully!"
                )

                st.rerun()

            except Exception as e:
                st.error(
                    f"Unable to create match: {e}"
                )
                # Edit Match
st.divider()
st.subheader("✏️ Edit Match")

matches_db = get_all_matches()

if matches_db:

    edit_match_options = {
        f"{match[4]} vs {match[6]} (ID: {match[0]})": match[0]
        for match in matches_db
    }

    selected_edit_match = st.selectbox(
        "Select Match to Edit",
        list(edit_match_options.keys()),
        key="edit_match_select"
    )

    selected_match_id = edit_match_options[selected_edit_match]

    selected_match = next(
        match for match in matches_db
        if match[0] == selected_match_id
    )

    (
        match_id,
        series_id,
        venue_id,
        team1_id,
        team1_name,
        team2_id,
        team2_name,
        match_type,
        match_date,
        status,
        winner_team_id,
        win_margin,
        victory_type,
    ) = selected_match

    team_options = {
        "India": 1,
        "Australia": 2,
        "England": 3,
        "South Africa": 4,
        "New Zealand": 5,
    }

    team1_index = (
        list(team_options.keys()).index(team1_name)
        if team1_name in team_options
        else 0
    )

    team2_index = (
        list(team_options.keys()).index(team2_name)
        if team2_name in team_options
        else 0
    )

    match_types = ["Test", "ODI", "T20", "T20I"]
    match_type_index = (
        match_types.index(match_type)
        if match_type in match_types
        else 0
    )

    statuses = ["upcoming", "live", "completed"]
    status_value = status.lower() if status else "upcoming"
    status_index = (
        statuses.index(status_value)
        if status_value in statuses
        else 0
    )

    with st.form("edit_match_form"):

        edit_team1 = st.selectbox(
            "Team 1",
            list(team_options.keys()),
            index=team1_index,
        )

        edit_team2 = st.selectbox(
            "Team 2",
            list(team_options.keys()),
            index=team2_index,
        )

        edit_match_type = st.selectbox(
            "Match Type",
            match_types,
            index=match_type_index,
        )

        edit_match_date = st.text_input(
            "Match Date",
            value=str(match_date or ""),
        )

        edit_status = st.selectbox(
            "Status",
            statuses,
            index=status_index,
        )

        submitted_edit = st.form_submit_button(
            "✏️ Update Match"
        )

        if submitted_edit:

            if edit_team1 == edit_team2:

                st.error(
                    "Team 1 and Team 2 must be different."
                )

            else:

                try:

                    updated = update_match(
                        match_id,
                        series_id,
                        venue_id,
                        team_options[edit_team1],
                        team_options[edit_team2],
                        edit_match_type,
                        edit_match_date,
                        edit_status,
                        winner_team_id,
                        win_margin,
                        victory_type,
                    )

                    if updated:

                        st.success(
                            "Match updated successfully!"
                        )

                        st.rerun()

                    else:

                        st.error("Match not found.")

                except Exception as e:

                    st.error(
                        f"Unable to update match: {e}"
                    )
                    # Delete Match
st.subheader("🗑️ Delete Match")

matches_db = get_all_matches()

if matches_db:

    delete_match_options = {
        f"{match[4]} vs {match[6]} (ID: {match[0]})": match[0]
        for match in matches_db
    }

    delete_match_name = st.selectbox(
        "Select Match to Delete",
        list(delete_match_options.keys()),
        key="delete_match_select"
    )

    if st.button("🗑️ Delete Match", type="secondary"):

        selected_delete_id = delete_match_options[delete_match_name]

        try:
            deleted = delete_match(selected_delete_id)

            if deleted:
                st.success(
                    "Match deleted successfully!"
                )
                st.rerun()
            else:
                st.error("Match not found.")

        except Exception as e:
            st.error(
                f"Unable to delete match: {e}"
            )