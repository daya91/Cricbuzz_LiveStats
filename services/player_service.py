from utils.db_connection import get_connection


def get_all_players():
    """Return all players from the database."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                player_id,
                player_name,
                team_id,
                role,
                batting_style,
                bowling_style
            FROM players
            ORDER BY player_name
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def create_player(
    player_id,
    player_name,
    team_id,
    role,
    batting_style,
    bowling_style,
):
    """Create a new player record."""
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO players
            (
                player_id,
                player_name,
                team_id,
                role,
                batting_style,
                bowling_style
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                player_id,
                player_name,
                team_id,
                role,
                batting_style,
                bowling_style,
            ),
        )

        connection.commit()

    finally:
        connection.close()