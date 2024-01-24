from .folder import FolderSaveArchiveRepo
from .s3 import S3SaveArchiveRepo


def save_archive_repo_factory(path, *args, **kwargs):
    if path.startswith('http'):
        archive = S3SaveArchiveRepo(path, *args, **kwargs)
    else:
        archive = FolderSaveArchiveRepo(path)

    return archive
