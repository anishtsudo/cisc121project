"""
Algorithm implementations for the interactive GUI demo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Iterable, List, Sequence


@dataclass(frozen=True)
class BubbleSortState:
    """
    Snapshot of the bubble sort algorithm at a specific iteration.

    Attributes
    ----------
    data:
        A copy of the list in its current state.
    index_a:
        The index of the first element being compared.
    index_b:
        The index of the second element being compared.
    swapped:
        Whether the current comparison resulted in a swap.
    pass_index:
        The current pass of the outer loop (0-based).
    """

    data: Sequence[int]
    index_a: int
    index_b: int
    swapped: bool
    pass_index: int


def bubble_sort_steps(values: Iterable[int]) -> Generator[BubbleSortState, None, List[int]]:
    """
    Perform bubble sort and yield intermediate states after each comparison.

    Parameters
    ----------
    values:
        Iterable containing integers to be sorted.

    Yields
    ------
    BubbleSortState
        The current state of the algorithm after each comparison, including swaps.

    Returns
    -------
    list[int]
        The sorted list of integers once the algorithm completes.
    """

    data = list(values)
    n = len(data)

    if n == 0:
        return data

    for pass_index in range(n - 1):
        swapped_in_pass = False

        for idx in range(n - pass_index - 1):
            swapped = False

            if data[idx] > data[idx + 1]:
                data[idx], data[idx + 1] = data[idx + 1], data[idx]
                swapped = True
                swapped_in_pass = True

            yield BubbleSortState(
                data=tuple(data),
                index_a=idx,
                index_b=idx + 1,
                swapped=swapped,
                pass_index=pass_index,
            )

        if not swapped_in_pass:
            break

    return data



