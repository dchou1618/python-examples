from collections import OrderedDict
from pydantic import BaseModel, Field
from typing import List

class SlidingWindowParam(BaseModel):
    s: str = Field(..., description="Input string", min_length=1)


def lengthOfLongestSubstringTwoDistinct(s: SlidingWindowParam) -> int:
    seen = OrderedDict()
    start = 0
    longest = 0
    for end in range(len(s)):
        if s[end] in seen:
            seen.move_to_end(s[end])
        seen[s[end]] = end
        if len(seen) > 2:
            _, idx = seen.popitem(last=False)
            start = idx+1
        longest = max(longest, end-start+1)
    return longest

def maximumUniqueSubarray(nums: List[int]) -> int:
    last_seen = dict()
    start, curr_sum, max_sum = 0, 0, 0
    for end in range(len(nums)):
        if nums[end] in last_seen:
            last_idx = last_seen[nums[end]] 
            if last_idx >= start:
                curr_sum -= sum(nums[start:(last_idx+1)])
                start = last_idx + 1
        curr_sum += nums[end]
        max_sum = max(max_sum, curr_sum)
        last_seen[nums[end]] = end
    return max_sum