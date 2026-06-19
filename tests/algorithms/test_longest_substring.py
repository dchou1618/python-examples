import pytest
from pydantic import ValidationError
from Algorithms.slidingWindow.longestUnique import lengthOfLongestSubstringTwoDistinct, maximumUniqueSubarray, SlidingWindowParam

# -------------------------
# Basic correctness tests
# -------------------------

@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("eceba", 3),
        ("ccaabbb", 5),
        ("ababffzzeee", 5),  
        ("aa", 2),
        ("a", 1),
        ("ab", 2),
        ("abc", 2),
    ],
)
def test_basic_cases(input_str, expected):
    param = SlidingWindowParam(s=input_str)
    assert lengthOfLongestSubstringTwoDistinct(param.s) == expected

@pytest.mark.parametrize(
    "nums, expected",
    [
        ([4, 2, 4, 5, 6], 17),          # example 1
        ([5, 2, 1, 2, 5, 2, 1, 2, 5], 8),  # example 2
        ([1], 1),
        ([1, 2], 3),
        ([1, 1], 1),
        ([1, 2, 3], 6),
        ([3, 3, 3], 3),
    ],
)
def test_basic_cases(nums, expected):
    assert maximumUniqueSubarray(nums) == expected

# -------------------------
# Regression / tricky cases
# -------------------------

def test_alternating_characters():
    param = SlidingWindowParam(s="abababab")
    assert lengthOfLongestSubstringTwoDistinct(param.s) == 8


def test_three_distinct_repeated():
    param = SlidingWindowParam(s="abcabcabc")
    assert lengthOfLongestSubstringTwoDistinct(param.s) == 2


def test_eviction_order_matters():
    # Breaks implementations that don't move_to_end
    param = SlidingWindowParam(s="abaccc")
    # Longest valid substring: "accc"
    assert lengthOfLongestSubstringTwoDistinct(param.s) == 4


def test_multiple_evictions():
    param = SlidingWindowParam(s="aabbccddeeff")
    assert lengthOfLongestSubstringTwoDistinct(param.s) == 4

def test_duplicate_at_start():
    # Forces window to jump start
    nums = [2, 1, 2, 3, 4]
    # Best: [1,2,3,4]
    assert maximumUniqueSubarray(nums) == 10


def test_duplicate_at_end():
    nums = [1, 2, 3, 4, 1]
    # Best: [1,2,3,4]
    assert maximumUniqueSubarray(nums) == 10


def test_multiple_duplicates():
    nums = [1, 2, 1, 3, 2, 3, 4]
    # Best: [1,3,2,3,4] is invalid
    # Best valid: [1,3,2] or [2,3,4]
    assert maximumUniqueSubarray(nums) == 9


def test_eviction_jump_needed():
    # Breaks incorrect start updates
    nums = [1, 2, 3, 2, 5]
    # Best: [3,2,5]
    assert maximumUniqueSubarray(nums) == 10

# -------------------------
# Edge cases
# -------------------------

def test_all_same_character():
    param = SlidingWindowParam(s="aaaaaaa")
    assert lengthOfLongestSubstringTwoDistinct(param.s) == 7


def test_two_characters_only():
    param = SlidingWindowParam(s="abababababab")
    assert lengthOfLongestSubstringTwoDistinct(param.s) == 12

def test_all_unique():
    nums = [1, 2, 3, 4, 5, 6]
    assert maximumUniqueSubarray(nums) == sum(nums)


def test_all_same():
    nums = [7, 7, 7, 7]
    assert maximumUniqueSubarray(nums) == 7


def test_large_values():
    nums = [10_000, 9_999, 10_000]
    assert maximumUniqueSubarray(nums) == 19_999

def test_strictly_increasing_then_repeat():
    nums = list(range(1, 100)) + [50]
    assert maximumUniqueSubarray(nums) == sum(range(1, 100))


def test_alternating_pattern():
    nums = [1, 2] * 50
    assert maximumUniqueSubarray(nums) == 3  # [1,2]

# -------------------------
# Pydantic validation tests
# -------------------------

def test_empty_string_rejected():
    with pytest.raises(ValidationError):
        SlidingWindowParam(s="")


def test_non_string_input():
    with pytest.raises(ValidationError):
        SlidingWindowParam(s=123)


# -------------------------
# Invariant-style tests
# -------------------------

@pytest.mark.parametrize("s", [
    "abc",
    "aabcbcdbca",
    "xyzzzyx",
    "pwwkew",
])
def test_result_never_exceeds_string_length(s):
    param = SlidingWindowParam(s=s)
    result = lengthOfLongestSubstringTwoDistinct(param.s)
    assert 0 < result <= len(s)

@pytest.mark.parametrize("nums", [
    [1, 2, 3],
    [1, 2, 1, 2, 3],
    [5, 5, 5, 1, 2],
    [100, 200, 300, 100, 400],
])
def test_result_never_exceeds_sum(nums):
    result = maximumUniqueSubarray(nums)
    assert 0 < result <= sum(nums)