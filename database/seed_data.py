import sqlite3


DATABASE_PATH = "database/cricket.db"


def seed_database():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        # Teams
        cursor.executemany(
            """
            INSERT OR IGNORE INTO teams
            (team_id, team_name, country, team_type)
            VALUES (?, ?, ?, ?)
            """,
            [
                (1, "India", "India", "International"),
                (2, "Australia", "Australia", "International"),
                (3, "England", "England", "International"),
                (4, "South Africa", "South Africa", "International"),
                (5, "New Zealand", "New Zealand", "International"),
            ],
        )

        # Players
        cursor.executemany(
            """
            INSERT OR IGNORE INTO players
            (player_id, player_name, team_id, role,
             batting_style, bowling_style)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    101,
                    "Virat Kohli",
                    1,
                    "Batter",
                    "Right-hand",
                    None,
                ),
                (
                    102,
                    "Rohit Sharma",
                    1,
                    "Batter",
                    "Right-hand",
                    None,
                ),
                (
                    103,
                    "Jasprit Bumrah",
                    1,
                    "Bowler",
                    "Right-hand",
                    "Right-arm Fast",
                ),
                (
                    201,
                    "Steve Smith",
                    2,
                    "Batter",
                    "Right-hand",
                    None,
                ),
                (
                    202,
                    "Pat Cummins",
                    2,
                    "Bowler",
                    "Right-hand",
                    "Right-arm Fast",
                ),
            ],
        )

        # Venues
        cursor.executemany(
            """
            INSERT OR IGNORE INTO venues
            (venue_id, venue_name, city, country, capacity)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    1,
                    "Wankhede Stadium",
                    "Mumbai",
                    "India",
                    33000,
                ),
                (
                    2,
                    "Melbourne Cricket Ground",
                    "Melbourne",
                    "Australia",
                    100000,
                ),
                (
                    3,
                    "Eden Gardens",
                    "Kolkata",
                    "India",
                    68000,
                ),
            ],
        )

        # Series
        cursor.executemany(
            """
            INSERT OR IGNORE INTO series
            (series_id, series_name, host_country,
             format, start_date, planned_matches)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    1,
                    "India vs Australia ODI Series",
                    "India",
                    "ODI",
                    "2024-09-01",
                    3,
                ),
                (
                    2,
                    "England Test Series",
                    "England",
                    "Test",
                    "2024-06-01",
                    5,
                ),
            ],
        )

        # Matches
        cursor.executemany(
            """
            INSERT OR IGNORE INTO matches
            (match_id, series_id, venue_id,
             team1_id, team2_id, match_type,
             match_date, status, winner_team_id,
             win_margin, victory_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    1001,
                    1,
                    1,
                    1,
                    2,
                    "ODI",
                    "2024-09-05",
                    "Completed",
                    1,
                    25,
                    "Runs",
                ),
                (
                    1002,
                    1,
                    2,
                    2,
                    1,
                    "ODI",
                    "2024-09-08",
                    "Completed",
                    2,
                    5,
                    "Wickets",
                ),
                (
                    1003,
                    2,
                    3,
                    3,
                    1,
                    "Test",
                    "2024-06-10",
                    "Completed",
                    3,
                    120,
                    "Runs",
                ),
            ],
        )

        # Player statistics
        cursor.executemany(
            """
            INSERT OR IGNORE INTO player_stats
            (stat_id, match_id, player_id,
             runs_scored, balls_faced, strike_rate,
             wickets_taken, runs_conceded, overs_bowled,
             economy_rate, catches, stumpings, batting_position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    1,
                    1001,
                    101,
                    85,
                    92,
                    92.39,
                    0,
                    0,
                    0,
                    0,
                    1,
                    0,
                    3,
                ),
                (
                    2,
                    1001,
                    102,
                    65,
                    70,
                    92.86,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                ),
                (
                    3,
                    1001,
                    103,
                    12,
                    15,
                    80.00,
                    4,
                    45,
                    10,
                    4.50,
                    2,
                    0,
                    9,
                ),
                (
                    4,
                    1002,
                    201,
                    72,
                    80,
                    90.00,
                    0,
                    0,
                    0,
                    0,
                    1,
                    0,
                    3,
                ),
                (
                    5,
                    1002,
                    202,
                    8,
                    12,
                    66.67,
                    3,
                    40,
                    10,
                    4.00,
                    1,
                    0,
                    10,
                ),
            ],
        )

        connection.commit()

        print("Sample data inserted successfully.")

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    seed_database()