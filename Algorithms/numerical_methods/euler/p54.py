from collections import defaultdict
from enum import IntEnum
from typing import Any, Dict, List

VALUE_MAP = {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

class Rank(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

def union_find_longest_consecutive(nums):
    parent = {}
    size = {}
    for x in nums:
        parent[x] = x
        size[x] = 1
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(a,b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        # assume rb is the smaller one
        parent[rb] = ra
        size[ra] += size[rb]
    snums = set(nums)
    for x in snums:
        if x+1 in snums:
            union(x, x+1)
    return max(size[find(x)] for x in nums)
    
def gather_hand_information(hand: List[str]) -> Dict[str, Any]:
    """
    return:
    - all_same_suit
    - value counts
    - are consecutive
    """
    seen = set()
    all_same = True
    d = defaultdict(int)
    vals = []
    for (val, suit) in [tuple(card) for card in hand]:
        if suit not in seen:
            if not seen:
                seen.add(suit)
            else:
                all_same = False
        int_val = VALUE_MAP[val] if val in VALUE_MAP else int(val)
        d[int_val] += 1
        vals.append(int_val)
    all_consecutive = (union_find_longest_consecutive(vals) == len(hand))
    return {"all_same_suit": all_same, 
            "value_counts": d,
            "all_consecutive": all_consecutive
    }

def determine_rank(player_info: Dict[str, Any]) -> tuple[Rank, tuple]:
    counts = player_info["value_counts"]

    # values sorted by (count, value)
    groups = sorted(
        ((cnt, val) for val, cnt in counts.items()),
        reverse=True
    )

    values_desc = sorted(counts.keys(), reverse=True)

    is_flush = player_info["all_same_suit"]
    is_straight = player_info["all_consecutive"]

    # Handle A2345 straight
    if set(counts.keys()) == {14, 2, 3, 4, 5}:
        is_straight = True
        straight_high = 5
    elif is_straight:
        straight_high = max(counts)
    else:
        straight_high = None

    if is_flush and is_straight:
        if straight_high == 14 and min(counts) == 10:
            return Rank.ROYAL_FLUSH, ()
        return Rank.STRAIGHT_FLUSH, (straight_high,)

    if groups[0][0] == 4:
        quad = groups[0][1]
        kicker = groups[1][1]
        return Rank.FOUR_OF_A_KIND, (quad, kicker)

    if groups[0][0] == 3 and groups[1][0] == 2:
        return Rank.FULL_HOUSE, (groups[0][1], groups[1][1])

    if is_flush:
        return Rank.FLUSH, tuple(values_desc)

    if is_straight:
        return Rank.STRAIGHT, (straight_high,)

    if groups[0][0] == 3:
        trip = groups[0][1]
        kickers = sorted(
            (v for v, c in counts.items() if c == 1),
            reverse=True,
        )
        return Rank.THREE_OF_A_KIND, (trip, *kickers)

    if groups[0][0] == 2 and groups[1][0] == 2:
        pairs = sorted(
            (v for v, c in counts.items() if c == 2),
            reverse=True,
        )
        kicker = next(v for v, c in counts.items() if c == 1)
        return Rank.TWO_PAIRS, (*pairs, kicker)

    if groups[0][0] == 2:
        pair = groups[0][1]
        kickers = sorted(
            (v for v, c in counts.items() if c == 1),
            reverse=True,
        )
        return Rank.ONE_PAIR, (pair, *kickers)

    return Rank.HIGH_CARD, tuple(values_desc)

def poker_hands(poker_file: str) -> int:
    player1_wins = 0
    with open(poker_file) as f:
        for row in f.readlines():
            vals = row.strip().split(" ")
            player1, player2 = vals[:5], vals[5:]
            player1_info = gather_hand_information(player1)
            player2_info = gather_hand_information(player2)
            rank1 = determine_rank(player1_info)
            rank2 = determine_rank(player2_info)
            if rank1 > rank2:
                player1_wins += 1
            elif rank1 == rank2:
                if max(player1_info["value_counts"].keys()) > max(player2_info["value_counts"].keys()):
                    player1_wins += 1
    return player1_wins
