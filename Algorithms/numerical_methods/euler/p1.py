def mult_35(n: int):
    v = 1
    s = 0
    while v < n:
        if v % 3 == 0 or v % 5 == 0:
            s += v
        v += 1
    return s