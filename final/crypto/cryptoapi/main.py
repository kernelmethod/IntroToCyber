from .crypto import encrypt
from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="CryptoAPI",
    version="0.0.1",
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

@app.post("/crypto/encrypt")
async def encrypt_file(file: UploadFile):
    """Encrypt a file."""

    filename = file.filename
    contents = await file.read()

    return encrypt(filename, contents)
