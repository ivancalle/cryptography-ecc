from typing import Tuple
from random import SystemRandom, Random
from base64 import b64encode, b64decode

from cryptography.hazmat.primitives.ciphers import Cipher as SymmetricCipher, algorithms, modes

from .curve import EllipticCurve
from .curve.solutions import Solution
from .curve.cicle import Cicle


class Cipher:
    def __init__(
            self,
            curve: EllipticCurve,
            g_point: Tuple[int, int],
            private_key: int | None = None
    ):
        self._curve = curve
        self._g_point = g_point
        self._g_solution = Solution(g_point[0], g_point[1], self._curve.param_a, self._curve.prime)
        self._cicle = Cicle(self._g_solution)
        if private_key is None:
            self._private_key = SystemRandom().randint(10, len(self._cicle))
        else:
            self._private_key = private_key

        self._public_key = self._g_solution*self._private_key
        self._common_secret: Tuple[int, int] | None = None

    @property
    def curve(self) -> EllipticCurve:
        return self._curve

    @property
    def g_point(self) -> Tuple[int, int]:
        return self._g_point

    def __str__(self):
        return f'Cipher{{ curve={self._curve}, g_point={self._g_point}, private_key={self._private_key}, public_key={tuple(self._public_key)} }}'

    def set_common_secret(self, public_key: Tuple[int, int]):
        sol = Solution(public_key[0], public_key[1], self._curve.param_a, self._curve.prime)
        self._common_secret = tuple(sol*self._private_key)

    def encrypt_AES(self, message: str) -> str:
        key = Random(self._common_secret[0]).getrandbits(256).to_bytes(32, 'big')
        iv = Random(self._common_secret[1]).getrandbits(128).to_bytes(16, 'big')

        cipher = SymmetricCipher(algorithms.AES(key), modes.CTR(iv))

        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(message.encode('utf8')) + encryptor.finalize()
        return b64encode(bytes(encrypted_message)).decode('utf-8')

    def decrypt_AES(self, encrypted_message: str) -> str:
        key = Random(self._common_secret[0]).getrandbits(256).to_bytes(32, 'big')
        iv = Random(self._common_secret[1]).getrandbits(128).to_bytes(16, 'big')

        cipher = SymmetricCipher(algorithms.AES(key), modes.CTR(iv))
        encrypted_message = b64decode(encrypted_message.encode('utf-8'))

        decryptor = cipher.decryptor()
        message = decryptor.update(encrypted_message) + decryptor.finalize()
        return message.decode('utf-8')
