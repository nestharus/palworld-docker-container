import os

from .repo import *
from ..factory import save_archive_factory
from ..folder import FolderSaveArchive


class FolderSaveArchiveRepo(SaveArchiveRepo):
    def __init__(self, path):
        path = os.path.relpath(path, start=os.getcwd())
        path = os.path.join('.', path)

        super().__init__(path)

    def list(self):
        backups = os.listdir(self.path)
        backups = [os.path.join(self.path, name) for name in backups]
        backups = sorted(backups, key=lambda file: os.path.basename(file), reverse=True)

        return backups

    def load(self, path):
        archive = save_archive_factory(path)

        archive.load()

        return archive
