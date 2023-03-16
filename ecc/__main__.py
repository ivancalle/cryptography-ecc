import argparse

from .cipher import Cipher
from .curve import EllipticCurve
from .key_generator import KeyGenerator

parser = argparse.ArgumentParser(prog='ecc')
group = parser.add_mutually_exclusive_group()
group.add_argument('--generate-key', '-g', action='store_true', help='Generate key')
group.add_argument('--decrypt', '-d', help='Decrypt private key', type=int)
group.add_argument('--encrypt', '-e', help='Encrypt private key', type=int)
group.required = True
opts, rem_args = parser.parse_known_args()
if not opts.generate_key:
    parser.add_argument('--message', '-m', required=True, help='Message')
    parser.add_argument('--curve', '-c', required=True, nargs=3, help='a b prime', type=int)
    parser.add_argument('--point', '-p', required=True, nargs=2, help='x y', type=int)
    parser.add_argument('--public_key', '-pk', required=True, nargs=2, help='public key of other cipher x y', type=int)


args = parser.parse_args()

if args.generate_key:
    key_generator = KeyGenerator()
    cipher1 = key_generator.get_cipher()
    cipher2 = Cipher(cipher1.curve, cipher1.g_point)
    print(cipher1)
    print(cipher2)
    # TODO mirar algo raro en la generación de public keys siempre salen con la misma x
elif args.decrypt:
    curve = EllipticCurve(*args.curve)
    g_point = tuple(args.point)
    cipher = Cipher(curve, g_point, private_key=args.decrypt)
    cipher.set_common_secret(tuple(args.public_key))
    print(cipher.decrypt_AES(args.message))

elif args.encrypt:
    curve = EllipticCurve(*args.curve)
    g_point = tuple(args.point)
    cipher = Cipher(curve, g_point, private_key=args.encrypt)
    cipher.set_common_secret(tuple(args.public_key))
    print(cipher.encrypt_AES(args.message))
