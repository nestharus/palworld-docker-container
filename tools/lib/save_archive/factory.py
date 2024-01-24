from .folder import FolderSaveArchive
from .s3 import S3SaveArchive
from .tar import TarSaveArchive


def save_archive_factory(path, *args, **kwargs):
    if path.startswith('http'):
        archive = S3SaveArchive(path, *args, **kwargs)
    elif path.endswith('.tar.gz'):
        archive = TarSaveArchive(path)
    else:
        archive = FolderSaveArchive(path)

    return archive
