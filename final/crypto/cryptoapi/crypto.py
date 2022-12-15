import os
from base64 import b64encode
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

ikm = os.environ["CRYPTO_IKM"].encode("utf-8")
if len(ikm) < 32:
    raise RuntimeError("Input key material must be at least 32 bytes")

hkdf = HKDF(SHA256(), length=32, salt=b"", info=b"Encrypt")
CHACHA_KEY: bytes = hkdf.derive(ikm)

hkdf = HKDF(SHA256(), length=32, salt=b"", info=b"GenerateNonce")
NONCE_KEY: bytes = hkdf.derive(ikm)


def encrypt(filename: str, contents: bytes):
    cipher = ChaCha20Poly1305(CHACHA_KEY)
    filename_as_bytes = filename.encode("utf-8")
    hkdf = HKDF(SHA256(), length=12, salt=b"", info=filename_as_bytes)
    nonce = hkdf.derive(NONCE_KEY)
    ciphertext = cipher.encrypt(nonce, contents, filename_as_bytes)

    # Poly1305 tag is stored in the last 16 bytes of the
    # ChaCha20Poly1305 output
    ct, tag = ciphertext[:-16], ciphertext[-16:]
    return {"ciphertext": b64encode(ct), "tag": b64encode(tag), "filename": filename}
