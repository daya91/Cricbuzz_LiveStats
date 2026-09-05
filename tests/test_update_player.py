from services.player_service import create_player, update_player, delete_player, get_all_players


def test_update_player():
    player_id = 997

    create_player(
        player_id,
        "Update Test Player",
        1,
        "Batter",
        "Right-hand",
        None,
    )

    updated = update_player(
        player_id,
        "Updated Test Player",
        2,
        "Bowler",
        "Left-hand",
        "Right-arm Fast",
    )

    assert updated == 1

    players = get_all_players()

    player = next(
        player for player in players
        if player[0] == player_id
    )

    assert player[1] == "Updated Test Player"
    assert player[2] == 2
    assert player[3] == "Bowler"
    assert player[4] == "Left-hand"
    assert player[5] == "Right-arm Fast"

    delete_player(player_id)