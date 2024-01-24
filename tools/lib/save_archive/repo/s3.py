import os

import boto3
from botocore.config import Config

from .repo import SaveArchiveRepo
from ..s3 import parse_s3_url, fetch_backup
from ..tar import TarSaveArchive, decompress_backup


class S3SaveArchiveRepo(SaveArchiveRepo):
    s3_host: str
    s3_bucket: str
    volume: str
    s3: any
    files: list

    def __init__(self, path, access_key, secret_access_key):
        super().__init__(path)

        self.s3_host, self.s3_bucket, self.volume = parse_s3_url(path)

        self.s3 = boto3.client('s3',
              endpoint_url=self.s3_host,
              aws_access_key_id=access_key,
              aws_secret_access_key=secret_access_key,
              config=Config(signature_version='s3v4')
        )

    def list(self):
        return fetch_backup_filenames(self.s3, self.s3_bucket, self.volume)

    def load(self, path):
        file = fetch_backup(self.s3, self.s3_bucket, path)
        archive = TarSaveArchive(path)

        archive.archive, archive.archive_info = decompress_backup(file)

        return archive


def fetch_backup_filenames(s3, bucket, volume):
    # List all directories in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucket, Delimiter='/')

    # Filter directories that contain a directory named S3_VOLUME
    filtered_dirs = []
    for content in response.get('CommonPrefixes', []):
        dir_name = content.get('Prefix')
        sub_response = s3.list_objects_v2(Bucket=bucket, Prefix=dir_name, Delimiter='/')
        for sub_content in sub_response.get('CommonPrefixes', []):
            if sub_content.get('Prefix').endswith(f'{volume}/'):
                filtered_dirs.append(dir_name)
                break

    file_list = []

    # Append each filename to the list
    for dir_name in filtered_dirs:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=dir_name)
        for content in response.get('Contents', []):
            file_list.append(content.get('Key'))

    # Sort the list by filename
    file_list = sorted(file_list, key=lambda file: os.path.basename(file), reverse=True)

    return file_list
