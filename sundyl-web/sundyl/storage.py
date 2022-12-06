"""Custom static and media storage using MinIO / S3."""

import os
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage
from sundyl.settings import CDN_DOMAIN


class StaticStorage(S3StaticStorage):
    bucket_name: str = os.getenv("WEB_STATIC_BUCKET", "www")
    custom_domain: str = f"{bucket_name}.{CDN_DOMAIN}"


class MediaStorage(S3Boto3Storage):
    bucket_name: str = os.getenv("WEB_MEDIA_BUCKET", "www-media")
    custom_domain: str = f"{bucket_name}.{CDN_DOMAIN}"
