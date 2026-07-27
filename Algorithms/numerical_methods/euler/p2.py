def even_fib(n: int):
    v1 = 1
    v2 = 2
    if n < 1:
        raise ValueError("n must be at least 1")
    elif n == 1:
        return 0
    else:
        s = 0
        while v2 <= n:
            if v2 % 2 == 0:
                s += v2
            temp = v2
            v2 = v2 + v1
            v1 = temp
        return s
