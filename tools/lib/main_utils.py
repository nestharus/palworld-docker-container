import os

from .save_archive.factory import save_archive_factory
from .save_archive.repo.factory import save_archive_repo_factory
from .save_archive.utils import get_game_profiles


def get_backup_repo(backup_directory):
    if backup_directory is None:
        S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
        S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
        S3_URL = os.getenv('S3_URL')

        backup_repo = save_archive_repo_factory(S3_URL, S3_ACCESS_KEY, S3_SECRET_KEY)
    else:
        backup_repo = save_archive_repo_factory(backup_directory)

    return backup_repo


def get_snapshot(path):
    save_archive = save_archive_factory(path)
    snapshot = save_archive.load()

    return snapshot


def find_game_profile(archive, profile_to_find):
    game_profiles = get_game_profiles(archive)

    if len(game_profiles) == 0:
        print(f'Unable to load archive with no game profiles')
        return

    if len(game_profiles) > 1 and profile_to_find is None:
        print(f'Unable to load archive with multiple game profiles and an unspecified profile to use')
        return

    if profile_to_find is None:
        game_profile = game_profiles[0]
    else:
        game_profiles = [
            profile
            for profile in game_profiles
            if profile == profile_to_find
        ]

        if len(game_profiles) == 1:
            game_profile = game_profiles[0]
        else:
            game_profile = None

    if game_profile is None:
        print(f'Unable to load archive with game profile {profile_to_find}')
        return None

    return game_profile
