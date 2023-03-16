from ..utils import is_prime
from .solutions import Solution
from .cicle import Cicle


class EllipticCurve:
    """Represent y²=x³+ax+b (mod p)"""

    def __init__(self, a: int, b: int, prime: int):
        if not is_prime(prime) or (4*a**3+27*b**2) % prime == 0:
            raise Exception('Invalid preconditions')

        self._a = a
        self._b = b
        self._prime = prime

    @property
    def param_a(self) -> int:
        return self._a

    @property
    def param_b(self) -> int:
        return self._b

    @property
    def prime(self) -> int:
        return self._prime

    def calculate_cicle_solutions(self, cicle_min):
        for y in range(1, self._prime):
            y2 = y**2
            for x in range(self._prime):
                if y2 % self._prime == (x**3+self._a*x+self._b) % self._prime:
                    cicle = Cicle(Solution(x, y, self._a, self._prime))
                    cicle_length = len(cicle)
                    if cicle_length >= cicle_min and is_prime(cicle_length):
                        break
            else:
                continue
            break
        else:
            raise Exception('No cicle solutions with the required conditions')

        return cicle

    def __str__(self):
        return f'EllipticCurve{{a={self._a},b={self._b},prime={self._prime}}}'
