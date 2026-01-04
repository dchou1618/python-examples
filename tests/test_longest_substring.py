import pytest
from pydantic import ValidationError
from Algorithms.slidingWindow.longestSubstring import lengthOfLongestSubstringTwoDistinct, SlidingWindowParam

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


# -------------------------
# Edge cases
# -------------------------

def test_all_same_character():
    param = SlidingWindowParam(s="aaaaaaa")
    assert lengthOfLongestSubstringTwoDistinct(param.s) == 7


def test_two_characters_only():
    param = SlidingWindowParam(s="abababababab")
    assert lengthOfLongestSubstringTwoDistinct(param.s) == 12


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
