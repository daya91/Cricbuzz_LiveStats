PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT NOT NULL,
    team_type TEXT
);

CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL,
    team_id INTEGER,
    role TEXT,
    batting_style TEXT,
    bowling_style TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY,
    venue_name TEXT NOT NULL,
    city TEXT,
    country TEXT,
    capacity INTEGER
);

CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY,
    series_name TEXT NOT NULL,
    host_country TEXT,
    format TEXT,
    start_date TEXT,
    planned_matches INTEGER
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    series_id INTEGER,
    venue_id INTEGER,
    team1_id INTEGER,
    team2_id INTEGER,
    match_type TEXT,
    match_date TEXT,
    status TEXT,
    winner_team_id INTEGER,
    win_margin INTEGER,
    victory_type TEXT,
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS player_stats (
    stat_id INTEGER PRIMARY KEY,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    runs_scored INTEGER DEFAULT 0,
    balls_faced INTEGER DEFAULT 0,
    strike_rate REAL,
    wickets_taken INTEGER DEFAULT 0,
    runs_conceded INTEGER DEFAULT 0,
    overs_bowled REAL DEFAULT 0,
    economy_rate REAL,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    batting_position INTEGER,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);