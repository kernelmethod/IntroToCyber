# Unit tests for the API

from io import BytesIO
from base64 import b64decode
from cryptoapi.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_encrypt_message():
    message = b"hello, world!"
    resp1 = client.post(
        "/crypto/encrypt",
        files={"file": ("myfile1", BytesIO(message), "application/octet-stream")},
    ).json()
    assert resp1["filename"] == "myfile1"
    assert "ciphertext" in resp1
    assert "tag" in resp1

    resp2 = client.post(
        "/crypto/encrypt",
        files={"file": ("myfile2", BytesIO(message), "application/octet-stream")},
    ).json()
    assert resp2["filename"] == "myfile2"
    assert resp1["ciphertext"] != resp2["ciphertext"]
    assert resp1["tag"] != resp2["tag"]

    resp3 = client.post(
        "/crypto/encrypt",
        files={"file": ("myfile1", BytesIO(message), "application/octet-stream")},
    ).json()
    assert resp1 == resp3


def test_perform_attack():
    msg1 = b"hello, world!"
    msg2 = b"aaaaaaaaaaaaa"

    resp1 = client.post(
        "/crypto/encrypt",
        files={"file": ("myfile", BytesIO(msg1), "application/octet-stream")},
    ).json()
    resp2 = client.post(
        "/crypto/encrypt",
        files={"file": ("myfile", BytesIO(msg2), "application/octet-stream")},
    ).json()

    ct1 = b64decode(resp1["ciphertext"])
    ct2 = b64decode(resp2["ciphertext"])

    xored_cts = bytes(b1 ^ b2 for (b1, b2) in zip(ct1, ct2))
    xored_msg = bytes(b1 ^ b2 for (b1, b2) in zip(msg1, msg2))
    assert xored_cts == xored_msg
