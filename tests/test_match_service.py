from services.match_service import (
    create_match,
    update_match,
    delete_match,
    get_all_matches,
)


def test_match_crud():
    match_id = 999

    # Create
    create_match(
        match_id,
        None,
        None,
        1,
        2,
        "Test Match",
        "2026-09-05",
        "completed",
        1,
        10,
        "runs",
    )

    matches = get_all_matches()

    assert any(
        match[0] == match_id
        for match in matches
    )

    # Update
    updated = update_match(
        match_id,
        None,
        None,
        1,
        2,
        "Updated Test Match",
        "2026-09-06",
        "completed",
        2,
        5,
        "wickets",
    )

    assert updated == 1

    matches = get_all_matches()

    match = next(
        match for match in matches
        if match[0] == match_id
    )

    assert match[7] == "Updated Test Match"
    assert match[8] == "2026-09-06"
    assert match[9] == "completed"
    assert match[10] == 2
    assert match[11] == 5
    assert match[12] == "wickets"

    # Delete
    deleted = delete_match(match_id)

    assert deleted == 1

    matches = get_all_matches()

    assert all(
        match[0] != match_id
        for match in matches
    )