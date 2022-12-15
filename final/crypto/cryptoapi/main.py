from .crypto import encrypt
from fastapi import FastAPI, UploadFile

app = FastAPI(
    title="CryptoAPI",
    version="0.0.1",
)


@app.post("/crypto/encrypt")
async def encrypt_file(file: UploadFile):
    """Encrypt a file."""

    filename = file.filename
    contents = await file.read()

    return encrypt(filename, contents)
