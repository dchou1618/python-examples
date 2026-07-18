from Algorithms.numerical_methods.euler import utils
from typing import List, Optional
import math

def possible_replacements(n: int, digit: int) -> List[int]:
    max_digits = math.floor(math.log(n, 10))+1
    def replace_digit(n: int, digit: int, pos: int):
        pos_val = (n % (10**pos)) // (10**(pos-1))
        new_n = n+(digit-pos_val) * (10**(pos-1))
        if pos == max_digits:
            return {new_n, n}
        else:
            return replace_digit(n, digit, pos+1) | replace_digit(new_n, digit, pos+1)
    return replace_digit(n, digit, pos=1)
    
def prime_digit_replacements(n: int, prime_family: int, start_point: Optional[int] = None) -> Optional[int]:
    """
    n: int 
    prime_family: int
    """
    is_prime, primes = utils.sieve(n)
    for p in primes:
        if start_point is not None and p < start_point:
            continue
        for digit in range(1, 10):
            valid_primes = 0
            for replacement in possible_replacements(p, digit):
                if is_prime[replacement]:
                    valid_primes += 1
            if valid_primes == prime_family:
                print(possible_replacements(p, digit))
                return p
    return None
