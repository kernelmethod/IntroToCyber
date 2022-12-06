#!/usr/bin/env python3

import argparse
import hashlib
import hmac
import random
import secrets
import sys
from math import ceil
from pathlib import Path
from base64 import b64encode

hash_len: int = 32

#################################################################

# Common helpers


def hmac_sha256(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def hkdf(key: str, info: str, salt: str = "", length: int = 32) -> bytes:
    """Key derivation function"""

    if len(salt) == 0:
        salt = bytes([0] * length)
    else:
        salt = salt.encode("utf-8")

    prk = hmac_sha256(salt, key.encode("utf-8"))
    t = b""
    okm = b""
    info = info.encode("utf-8")

    for i in range(ceil(length / hash_len)):
        t = hmac_sha256(prk, t + info + bytes([i + 1]))
        okm += t
    return okm[:length]


def generate_domain_key(args):
    with open(args.key_file, "r") as f:
        key = f.readline().rstrip()

    # Stuff the length into the info parameter, so that two keys with the same
    # domain but different lengths are different
    info = f"length={args.length};{args.info}"
    salt = "" if args.salt is None else args.salt
    okm = hkdf(key, info, salt, length=args.length)
    return okm
    digest = b64encode(okm).decode()
    return digest


#################################################################

# Subcommands


def generate_key(args):
    n_bytes = args.n_bytes
    key = secrets.token_bytes(n_bytes)
    key = b64encode(key).decode()
    print(key)


def domain_key(args):
    okm = generate_domain_key(args)
    print(b64encode(okm).decode())


def random_word(args):
    """Read a random word from a wordlist."""

    okm = generate_domain_key(args)

    # random.choice is not cryptographically random, but the seed is, and for our
    # purposes that's good enough
    seed = int.from_bytes(okm, "big")
    random.seed(seed)

    with open(args.wordlist, "r") as f:
        words = f.read().splitlines()

    print(random.choice(words))


def random_int(args):
    """Generate a random integer."""

    okm = generate_domain_key(args)

    # This suffers the same problem as random_word, but again, it doesn't matter
    # very much.
    seed = int.from_bytes(okm, "big")
    random.seed(seed)

    print(random.randint(args.low, args.high))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=Path(__file__).name,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.set_defaults(func=lambda args: parser.print_help(sys.stderr))
    subparsers = parser.add_subparsers(title="subcommands")

    cmd_generate_key = subparsers.add_parser(
        "generate_key",
        help="Create IKM for flag generation"
    )
    cmd_generate_key.set_defaults(func=generate_key)
    cmd_generate_key.add_argument(
        "-l", "--length",
        dest="n_bytes",
        type=int,
        default=24,
        help="Size of generated IKM in bytes",
    )

    cmd_domain = subparsers.add_parser(
        "domain",
        help="Generate domain-specific OKM",
    )
    cmd_domain.set_defaults(func=domain_key)

    cmd_word = subparsers.add_parser(
        "word",
        help="Generate random word from wordlist using OKM",
    )
    cmd_word.set_defaults(func=random_word)

    cmd_int = subparsers.add_parser(
        "int",
        help="Generate random integer using OKM",
    )
    cmd_int.set_defaults(func=random_int)

    for sp in (cmd_domain, cmd_word, cmd_int):
        sp.add_argument(
            "-k",
            "--key-file",
            type=str,
            required=True,
            help="The path to the file containing the secret key",
        )
        sp.add_argument(
            "-s",
            "--salt",
            default=None,
            required=False,
            help="The salt to use",
        )
        sp.add_argument(
            "info",
            help="Domain separation parameter for the key to be generated",
        )
        sp.add_argument(
            "-l", "--length",
            type=int,
            default=12,
            help="Key length to generate (bytes)",
        )

    cmd_word.add_argument(
        "wordlist",
        help="The wordlist to read from",
    )

    cmd_int.add_argument(
        "--low",
        type=int,
        required=True,
        default=0,
        help="Lower bound on random integer that should be generated",
    )
    cmd_int.add_argument(
        "--high",
        type=int,
        required=True,
        default=2**16,
        help="Upper bound on random integer that should be generated",
    )

    args = parser.parse_args()
    args.func(args)
