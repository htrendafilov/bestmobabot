from __future__ import annotations

from typing import List

import pytest

from bestmobabot.itertools_ import secretary_max, slices


@pytest.mark.parametrize('n, length, expected', [
    (1, 5, [slice(0, 5)]),
    (3, 5, [slice(0, 5), slice(5, 10), slice(10, 15)]),
])
def test_slices(n: int, length: int, expected: List[slice]):
    assert slices(n, length) == expected


@pytest.mark.parametrize('items, expected, next_', [
    ([0], 0, None),
    ([100], 100, None),
    ([100, 45], 100, 45),
    ([0, 1], 0, 1),
    ([45, 100], 45, 100),
    ([1, 4, 5], 4, 5),
    ([1, 5, 4], 5, 4),
    ([5, 4, 1], 1, None),
    ([5, 1, 4], 4, None),
    ([4, 1, 5], 5, None),
    ([56, 7, 37, 73, 90, 59, 65, 61, 29, 16, 47, 77, 60, 8, 1, 76, 36, 68, 34, 17, 23, 26, 12, 82, 52, 88, 45, 89, 94, 81, 3, 24, 43, 55, 38, 33, 15, 92, 79, 87, 14, 75, 41, 98, 31, 58, 53, 72, 39, 30, 2, 0, 49, 99, 28, 50, 80, 91, 83, 27, 64, 71, 93, 95, 11, 21, 6, 66, 51, 85, 48, 62, 22, 74, 69, 63, 86, 57, 97, 32, 84, 4, 18, 46, 20, 42, 25, 35, 9, 10, 19, 40, 54, 67, 70, 5, 44, 13, 78, 96], 98, 31),  # noqa
    ([10, 68, 52, 48, 81, 39, 85, 54, 3, 21, 31, 59, 28, 64, 42, 90, 79, 12, 63, 41, 58, 57, 13, 43, 74, 76, 94, 51, 99, 67, 49, 14, 6, 96, 18, 17, 32, 73, 56, 7, 16, 60, 61, 26, 86, 72, 20, 62, 4, 83, 15, 55, 70, 29, 23, 35, 77, 98, 92, 22, 38, 5, 50, 82, 1, 84, 93, 97, 65, 37, 45, 71, 25, 11, 19, 75, 78, 44, 46, 2, 53, 36, 0, 47, 88, 24, 80, 66, 87, 40, 69, 27, 9, 8, 91, 89, 34, 33, 95, 30], 30, None),  # noqa
])
def test_secretary_max(items, expected, next_):
    """
    https://codegolf.stackexchange.com/questions/75967/solve-the-secretary-problem
    """
    iterator = iter(items)
    assert secretary_max(iterator, len(items)) == expected
    assert next(iterator, None) == next_  # test the iterator position


@pytest.mark.parametrize('items, early_stop, expected, next_', [
    ([0], 42, 0, None),
    ([100], 42, 100, None),
    ([100, 45], 42, 100, 45),
    ([0, 1], 42, 0, 1),
    ([45, 100], 42, 45, 100),
    ([1, 4, 5], 1, 1, 4),
    ([1, 5, 4], 5, 5, 4),
    ([5, 4, 1], 4, 5, 4),
    ([5, 1, 4], 5, 5, 1),
    ([4, 1, 5], 1, 4, 1),
])
def test_secretary_max_early_stop(items, early_stop, expected, next_):
    iterator = iter(items)
    assert secretary_max(iterator, len(items), early_stop=early_stop) == expected
    assert next(iterator, None) == next_  # test the iterator position
