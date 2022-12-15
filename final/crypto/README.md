# Crypto challenge

This directory contains the source code for the cryptography question for the
final exam.

## About the code

The primary cryptographic code is defined in `cryptoapi/crypto.py`, which
presents a basic "file encryption" function (used by the `/crypto/encrypt`
endpoint of the server).

The endpoint in question has a nonce reuse vulnerability. Instead of ensuring
that messages are encrypted with unique nonces, the server generates a random
nonce using HKDF-SHA-256 with the `NONCE_KEY` and the filename in the info
parameter.

As a result, two files sharing the same filename will be encrypted with the same
`(key, nonce)` pair. To decrypt an arbitrary file, you can send a file to the
API whose contents you know (e.g., containing all null bytes), XOR its
ciphertext with the encrypted file, and then XOR the result again with the known
plaintext.
