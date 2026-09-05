from services.player_service import create_player, delete_player, get_all_players


def test_create_player():
    player_id = 998

    create_player(
        player_id,
        "Create Test Player",
        1,
        "Batter",
        "Right-hand",
        None,
    )

    players = get_all_players()

    assert any(
        player[0] == player_id and player[1] == "Create Test Player"
        for player in players
    )

    delete_player(player_id)