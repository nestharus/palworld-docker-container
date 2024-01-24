import os


def get_separator(folders):
    if not folders:
        return os.sep

    for folder in folders:
        if '/' in folder:
            return '/'
        elif '\\' in folder:
            return '\\'

    return os.sep


def get_player_guids(files, game_profile_folder):
    sep = get_separator(files.keys())

    guids = [
        file.split(sep)[-1].split('.')[0]
        for file in files.keys()
        if file.startswith(f'{game_profile_folder}{sep}Players{sep}')
    ]

    guids = [
        guid[:8] + '-' + guid[8:12] + '-' + guid[12:16] + '-' + guid[16:20] + '-' + guid[20:]
        for guid in guids
    ]

    return guids


def get_game_profile_folder(files, game_profile):
    sep = get_separator(files.keys())

    folders = [
        file
        for file, file_content in files.items()
        if file_content is None
    ]

    folders = [
        folder
        for folder in folders
        if not folder.endswith('.sav')
    ]

    player_folders = [
        folder
        for folder in folders
        if folder.endswith(sep + 'Players')
    ]

    game_profiles = [
        sep.join(player_folder.split(sep)[:-1])
        for player_folder in player_folders
        if player_folder.split(sep)[-2] == game_profile
    ]

    if len(game_profiles) == 0:
        return None

    return game_profiles[0]


def get_archive_files(files):
    sep = get_separator(files.keys())

    files = {
        file
        for file in files.keys()
        if file.endswith('.sav')
    }

    files = {
        file.replace('.' + sep, '')
        for file in files
    }

    return files


def get_archive_folders(files):
    folders = [
        file
        for file in files.keys()
        if not file.endswith('.sav')
    ]

    return folders


def get_game_profiles(files):
    sep = get_separator(files.keys())
    folders = get_archive_folders(files)

    player_folders = [
        folder
        for folder in folders
        if folder.endswith(sep + 'Players')
    ]

    game_profiles = [
        player_folder.split(sep)[-2]
        for player_folder in player_folders
    ]

    return game_profiles


def get_player_file(files, game_profile_folder, guid):
    sep = get_separator(files.keys())
    guid = guid.replace('-', '')

    return f'{game_profile_folder}{sep}Players{sep}{guid}.sav'


def get_player_files(files, game_profile_folder):
    sep = get_separator(files.keys())

    files = [
        file
        for file in files.keys()
        if file.startswith(f'{game_profile_folder}{sep}Players{sep}')
    ]

    return files


def get_level_file(files, game_profile_folder):
    sep = get_separator(files.keys())

    files = [
        file
        for file in files.keys()
        if file.endswith(f'{sep}Level.sav') and file.startswith(game_profile_folder)
    ]

    if len(files) == 0:
        return None

    return files[0]


def get_level_meta_file(files, game_profile_folder):
    sep = get_separator(files.keys())

    files = [
        file
        for file in files.keys()
        if file.endswith(f'{sep}LevelMeta.sav') and file.startswith(game_profile_folder)
    ]

    if len(files) == 0:
        return None

    return files[0]
