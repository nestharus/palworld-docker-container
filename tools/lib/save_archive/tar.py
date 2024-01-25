import io
import tarfile

from .archive import SaveArchive


class TarSaveArchive(SaveArchive):
    def __init__(self, path):
        super().__init__(path)

    def load(self):
        with open(self.path, 'rb') as f:
            archive = f.read()
        self.archive, self.archive_info = decompress_backup(archive)

        return self.archive

    def save_as(self, path=None, archive=None):
        if archive is None:
            archive = self.archive

        if path is None:
            path = self.path

        with open(path, 'wb') as f:
            f.write(compress_backup(archive, self.archive_info))


def decompress_backup(file_data):
    file_obj = io.BytesIO(file_data)
    files = {}
    tar_info = {}

    with tarfile.open(fileobj=file_obj, mode='r:gz') as tar:
        for member in tar.getmembers():
            if member.isfile():
                f = tar.extractfile(member)
                if f is not None:
                    content = f.read()
                    files[member.name] = content
            elif member.isdir():
                # Store the directory in the dictionary with a value of None
                files[member.name] = None
            # Store the TarInfo object in the dictionary
            tar_info[member.name] = member

    return files, tar_info


def compress_backup(files, tar_info):
    tar_data = io.BytesIO()

    with tarfile.open(fileobj=tar_data, mode='w:gz') as tar:
        # First, add directories
        for file_name, file_content in sorted(files.items()):
            info = tar_info[file_name]
            if file_content is None:
                print(file_name)
                tar.addfile(info)

        # Then, add files
        for file_name, file_content in files.items():
            info = tar_info[file_name]
            if file_content is not None:
                print(file_name)
                info.size = len(file_content)
                if len(file_content) == 0:
                    tar.addfile(info)
                else:
                    tar.addfile(info, io.BytesIO(file_content))

    tar_data.seek(0)

    return tar_data.getvalue()
