def sum_squares(n: int):
    if n < 1:
        raise ValueError("n must be specified for first n sum squares")
    s = 0
    for i in range(1, n+1):
        v = i*i
        if v % 2 != 0:
            s += v
    return s