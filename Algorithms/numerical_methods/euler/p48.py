
def self_powers(n: int):
    if n < 1:
        raise ValueError("n must be at least 1")
    res = 0
    MOD = 10**10
    for i in range(1, n+1):
        res = (res + pow(i, i, MOD)) % MOD 
    return res