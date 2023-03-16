from typing import List


def get_factors(number: int, start: int = 2) -> List[int]:
    for i in range(start, number//2+1):
        if number % i == 0:
            return [i]+(get_factors(number//i, i))
    return [number]


def is_prime(number: int) -> bool:
    for x in range(2, int(number/2)+1):
        if number % x == 0:
            return False
    return True
