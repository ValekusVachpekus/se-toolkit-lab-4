"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    # item_id=1, learner_id=2 — ids differ; filtering by item_id=1 should include it
    interactions = [_make_log(1, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].item_id == 1
    assert result[0].learner_id == 2


def test_filter_returns_empty_when_no_item_id_matches() -> None:
    interactions = [_make_log(1, 1, 2), _make_log(2, 2, 3)]
    result = _filter_by_item_id(interactions, 99)
    assert result == []


def test_filter_returns_empty_for_single_non_matching_item() -> None:
    result = _filter_by_item_id([_make_log(1, 1, 5)], 6)
    assert result == []


def test_filter_returns_entire_list_when_all_items_match_item_id() -> None:
    interactions = [_make_log(1, 1, 7), _make_log(2, 2, 7), _make_log(3, 3, 7)]
    result = _filter_by_item_id(interactions, 7)
    assert result == interactions


def test_filter_returns_only_matching_subset_from_mixed_list() -> None:
    interactions = [
        _make_log(1, 1, 3),
        _make_log(2, 2, 4),
        _make_log(3, 3, 3),
        _make_log(4, 4, 5),
    ]
    result = _filter_by_item_id(interactions, 3)
    assert len(result) == 2
    assert all(i.item_id == 3 for i in result)


def test_filter_with_zero_as_item_id() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 1
    assert result[0].item_id == 0
