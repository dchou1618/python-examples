from collections import OrderedDict
from pydantic import BaseModel, Field

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