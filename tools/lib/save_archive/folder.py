import os
import io

from .archive import SaveArchive


class FolderSaveArchive(SaveArchive):
    def __init__(self, path):
        path = os.path.relpath(path, start=os.getcwd())
        path = os.path.join('.', path)

        super().__init__(path)

    def load(self):
        self.archive = read_folder_save_archive(self.path)
        self.archive_info = None

        return self.archive

    def save_as(self, path=None, archive=None):
        if archive is None:
            archive = self.archive

        if path is None:
            path = self.path

        if path != self.path:
            archive = {
                os.path.join(path, key[len(self.path) + 1:]): value
                for key, value in self.archive.items()
            }

        write_folder_save_archive(archive)


def read_folder_save_archive(folder):
    file_dict = {}
    for dirpath, dirnames, filenames in os.walk(folder):
        for dirname in dirnames:
            directory_path = os.path.join(dirpath, dirname)
            file_dict[directory_path] = None
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            with io.open(filepath, 'rb') as file:
                file_dict[filepath] = file.read()
    return file_dict


def write_folder_save_archive(files):
    for file_name, file_content in files.items():
        if file_content is None:
            continue

        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, 'wb') as f:
            f.write(file_content)
