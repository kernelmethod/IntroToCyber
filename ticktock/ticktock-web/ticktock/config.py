# Global configuration

import os
import typing as _t
from pathlib import Path

# Database configuration
DB_USER: str = os.environ["POSTGRES_USER"]
DB_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
DB_NAME: str = os.environ["POSTGRES_DB"]
DB_HOST: str = os.environ["DB_HOST"]
db_uri: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
max_post_len: int = 1024

# S3 configuration
buckets: _t.Final[dict] = {
    "avatar": os.environ["MINIO_BUCKET_AVATARS"],
}

# Flask configuration
template_folder: _t.Final[Path] = Path(__file__).parent / "templates"
static_folder: _t.Final[Path] = Path(__file__).parent / "static"

# Default path for other files
misc_files: _t.Final[Path] = Path(__file__).parent / "misc"
wordlists: _t.Final[Path] = misc_files / "wordlists"
misc_img: _t.Final[Path] = misc_files / "img"

# Default logfile
logfile: Path = "/var/log/ticktock/ticktock.log"
