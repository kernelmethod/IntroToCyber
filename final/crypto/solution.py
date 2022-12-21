#!/usr/bin/env python3

"""
**NOTE:** in practice, I wouldn't recommend going to all the trouble of using
the `requests` library to make a POST request to the webserver. You can get by
just doing everything manually, by copying the "ciphertext" fields of the
encrypted_manifesto.txt.json file and a file you upload to the attacker's
webserver into a single Python script.
"""

import json
import requests
from base64 import b64decode

def xor(a: bytes, b: bytes) -> bytes:
    return bytes(a_i ^ b_i for (a_i, b_i) in zip(a, b))

URL = "http://crypto.fr3ddy.lab:1337/crypto/encrypt"

with open("encrypted_manifesto.txt.json", "r") as f:
    encrypted_file = json.load(f)

filename = encrypted_file["filename"]

dummy_file = f"/tmp/{filename}"
dummy_file_contents = b"a" * 2048

with open(dummy_file, "wb") as f:
    f.write(dummy_file_contents)

# Upload dummy file, with the same name as the encrypted file, to the server
with open(dummy_file, "rb") as f:
    resp = requests.post(URL, files={"file": f}).json()

# Now compute the original plaintext with
#
#       m_1 = C_1 ⊕ C_2 ⊕ m_2
#
C_1 = b64decode(encrypted_file["ciphertext"])
C_2 = b64decode(resp["ciphertext"])
m_2 = dummy_file_contents

m_1 = xor(xor(C_1, C_2), m_2).decode()
print(m_1)
