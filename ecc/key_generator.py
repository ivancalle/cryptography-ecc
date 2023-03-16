from random import SystemRandom
from typing import Tuple

from .utils import is_prime
from .curve import EllipticCurve
from .cipher import Cipher


class KeyGenerator:
    def __init__(
        self,
        seed: int | None = None,
        prime_min: int = 10,
        prime_max=100,
        constant_min: int = 10,
        constant_max=100,
        cicle_length_min: int = 100,
        key_gen_tries: int = 1000,
    ) -> None:
        self._random = SystemRandom(seed)
        self._prime_min = prime_min
        self._prime_max = prime_max
        self._constant_min = constant_min
        self._constant_max = constant_max
        self._cicle_length_min = cicle_length_min
        self._key_gen_tries = key_gen_tries

    def _get_prime(self) -> int:
        diff = self._prime_max-self._prime_min
        start = self._random.randint(0, diff)
        for i in range(diff+1):
            number = self._prime_min+(start+i) % (diff+1)
            if is_prime(number):
                return number

        raise Exception('Prime not found')

    def _get_encription_params(self) -> Tuple[EllipticCurve, Tuple[int, int]]:
        prime = self._get_prime()
        constant_a = self._random.randint(self._constant_min, self._constant_max)
        constant_b = self._random.randint(self._constant_min, self._constant_max)
        curve = EllipticCurve(constant_a, constant_b, prime)
        solutions = curve.calculate_cicle_solutions(self._cicle_length_min)
        g_point = self._random.choice(list(solutions)[:-1])

        return (curve, tuple(g_point))

    def get_cipher(self) -> Cipher | None:
        for _ in range(self._key_gen_tries):
            try:
                curve, g_point = self._get_encription_params()
                return Cipher(curve, g_point)
            except Exception:
                pass
