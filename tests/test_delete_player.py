from services.player_service import create_player, delete_player, get_all_players


def test_delete_player():
    player_id = 999

    create_player(
        player_id,
        "Delete Test Player",
        1,
        "Batter",
        "Right-hand",
        None,
    )

    deleted = delete_player(player_id)

    assert deleted == 1

    players = get_all_players()

    assert all(player[0] != player_id for player in players)