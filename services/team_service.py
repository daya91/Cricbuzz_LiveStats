from utils.db_connection import get_connection


def get_all_teams():
    """Return all teams."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                team_id,
                team_name,
                country,
                team_type
            FROM teams
            ORDER BY team_name
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def create_team(
    team_id,
    team_name,
    country,
    team_type,
):
    """Create a new team."""
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO teams
            (
                team_id,
                team_name,
                country,
                team_type
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                team_id,
                team_name,
                country,
                team_type,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def update_team(
    team_id,
    team_name,
    country,
    team_type,
):
    """Update an existing team."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE teams
            SET
                team_name = ?,
                country = ?,
                team_type = ?
            WHERE team_id = ?
            """,
            (
                team_name,
                country,
                team_type,
                team_id,
            ),
        )

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()


def delete_team(team_id):
    """Delete an existing team."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM teams
            WHERE team_id = ?
            """,
            (team_id,),
        )

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()