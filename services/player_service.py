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
def update_player(
    player_id,
    player_name,
    team_id,
    role,
    batting_style,
    bowling_style,
):
    """Update an existing player record."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE players
            SET
                player_name = ?,
                team_id = ?,
                role = ?,
                batting_style = ?,
                bowling_style = ?
            WHERE player_id = ?
            """,
            (
                player_name,
                team_id,
                role,
                batting_style,
                bowling_style,
                player_id,
            ),
        )

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()
def delete_player(player_id):
    """Delete an existing player record."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM players
            WHERE player_id = ?
            """,
            (player_id,),
        )

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()