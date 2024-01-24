from typing import Union
from urllib.parse import urlparse

import boto3
from botocore.config import Config

from .archive import SaveArchive
from .tar import TarSaveArchive, decompress_backup, compress_backup


class S3SaveArchive(SaveArchive):
    s3_host: str
    s3_bucket: str
    volume: str
    s3: any
    tar_archive: Union[any, None]

    def __init__(self, path, access_key, secret_access_key):
        super().__init__(path)

        self.s3_host, self.s3_bucket, self.volume = parse_s3_url(path)

        self.s3 = boto3.client('s3',
            endpoint_url=self.s3_host,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version='s3v4')
        )

    def load(self):
        file = fetch_backup(self.s3, self.s3_bucket, self.path)
        self.tar_archive = TarSaveArchive(self.path)

        self.tar_archive.archive, self.tar_archive.archive_info = decompress_backup(file)

        return self.tar_archive.archive

    def save_as(self, path=None, archive=None):
        if archive is None:
            archive = self.tar_archive.archive

        if path is None:
            path = self.path

        data = compress_backup(archive, self.tar_archive.archive_info)

        put_backup(self.s3, self.s3_bucket, path, data)


def parse_s3_url(s3_url):
    parsed_url = urlparse(s3_url)

    host = parsed_url.netloc
    path_parts = parsed_url.path.lstrip('/').split('/', 1)

    bucket_name = path_parts[0]
    path_name = path_parts[1] if len(path_parts) > 1 else ''

    return host, bucket_name, path_name


def fetch_backup(s3, bucket, file_name):
    response = s3.get_object(Bucket=bucket, Key=file_name)
    file_data = response['Body'].read()

    return file_data


def put_backup(s3, bucket, file_name, data):
    s3.put_object(Bucket=bucket, Key=file_name, Body=data)
