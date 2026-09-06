from services.team_service import (
    create_team,
    update_team,
    delete_team,
    get_all_teams,
)


def test_team_crud():
    team_id = 998

    # Create
    create_team(
        team_id,
        "Test Team",
        "Test Country",
        "International",
    )

    teams = get_all_teams()

    assert any(
        team[0] == team_id and team[1] == "Test Team"
        for team in teams
    )

    # Update
    updated = update_team(
        team_id,
        "Updated Test Team",
        "Updated Country",
        "Domestic",
    )

    assert updated == 1

    teams = get_all_teams()

    team = next(
        team for team in teams
        if team[0] == team_id
    )

    assert team[1] == "Updated Test Team"
    assert team[2] == "Updated Country"
    assert team[3] == "Domestic"

    # Delete
    deleted = delete_team(team_id)

    assert deleted == 1

    teams = get_all_teams()

    assert all(
        team[0] != team_id
        for team in teams
    )