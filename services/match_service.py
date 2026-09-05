from utils.db_connection import get_connection


def get_all_matches():
    """Return all matches with team names."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                m.match_id,
                m.series_id,
                m.venue_id,
                m.team1_id,
                t1.team_name AS team1_name,
                m.team2_id,
                t2.team_name AS team2_name,
                m.match_type,
                m.match_date,
                m.status,
                m.winner_team_id,
                m.win_margin,
                m.victory_type
            FROM matches m
            LEFT JOIN teams t1
                ON m.team1_id = t1.team_id
            LEFT JOIN teams t2
                ON m.team2_id = t2.team_id
            ORDER BY m.match_date DESC
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def create_match(
    match_id,
    series_id,
    venue_id,
    team1_id,
    team2_id,
    match_type,
    match_date,
    status,
    winner_team_id,
    win_margin,
    victory_type,
):
    """Create a new match."""
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO matches
            (
                match_id,
                series_id,
                venue_id,
                team1_id,
                team2_id,
                match_type,
                match_date,
                status,
                winner_team_id,
                win_margin,
                victory_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                match_id,
                series_id,
                venue_id,
                team1_id,
                team2_id,
                match_type,
                match_date,
                status,
                winner_team_id,
                win_margin,
                victory_type,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def update_match(
    match_id,
    series_id,
    venue_id,
    team1_id,
    team2_id,
    match_type,
    match_date,
    status,
    winner_team_id,
    win_margin,
    victory_type,
):
    """Update an existing match."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE matches
            SET
                series_id = ?,
                venue_id = ?,
                team1_id = ?,
                team2_id = ?,
                match_type = ?,
                match_date = ?,
                status = ?,
                winner_team_id = ?,
                win_margin = ?,
                victory_type = ?
            WHERE match_id = ?
            """,
            (
                series_id,
                venue_id,
                team1_id,
                team2_id,
                match_type,
                match_date,
                status,
                winner_team_id,
                win_margin,
                victory_type,
                match_id,
            ),
        )

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()


def delete_match(match_id):
    """Delete an existing match."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM matches
            WHERE match_id = ?
            """,
            (match_id,),
        )

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()