from typing import Union


class SaveArchive:
    archive: Union[dict, None]
    archive_info: Union[dict, None]

    def __init__(self, path):
        self.path = path
        self.archive = None
        self.archive_info = None

    def load(self):
        pass

    def save_as(self, path, archive):
        pass
