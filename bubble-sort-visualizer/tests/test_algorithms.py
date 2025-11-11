"""
Tests for the bubble sort algorithm demo.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from algorithms import BubbleSortState, bubble_sort_steps


def test_bubble_sort_steps_completes_sorted_sequence():
    values = [5, 1, 4, 2, 8]
    generator = bubble_sort_steps(values)

    for _ in generator:
        pass

    # When the generator finishes, the sorted list is returned as StopIteration.value
    try:
        next(generator)
    except StopIteration as exc:
        assert exc.value == sorted(values)
    else:
        raise AssertionError("Generator should have been exhausted and returned a value.")


def test_bubble_sort_states_are_dataclasses():
    values = [3, 2, 1]
    state = next(bubble_sort_steps(values))
    assert isinstance(state, BubbleSortState)
    assert hasattr(state, "data")
    assert hasattr(state, "index_a")
    assert hasattr(state, "index_b")
    assert hasattr(state, "swapped")
    assert hasattr(state, "pass_index")


def test_bubble_sort_early_exit_on_sorted_input():
    values = [1, 2, 3, 4]
    generator = bubble_sort_steps(values)
    states = list(generator)
    # Already sorted list should complete in n-1 comparisons without swaps
    assert len(states) == len(values) - 1
    assert all(not state.swapped for state in states)

