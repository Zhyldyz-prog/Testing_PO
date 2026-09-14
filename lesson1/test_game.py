from game_logic import check_choice, add_score, is_game_finished
import pytest


def test_game_not_finished():
    assert is_game_finished(5) == False


def test_game_finished():
    assert is_game_finished(11) == True


def test_add_score():
    assert add_score(0) == 1


def test_add_score_to_existing():
    assert add_score(5) == 6


def test_heads():
    assert check_choice('орёл') == 'heads'


def test_tails():
    assert check_choice('решка') == 'tails'


def test_invalid_choice():
    with pytest.raises(ValueError):
        check_choice('яблоко')