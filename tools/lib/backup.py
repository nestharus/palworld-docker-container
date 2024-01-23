import os
import tarfile
import io


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


def fetch_backup(s3, bucket, file_name):
    response = s3.get_object(Bucket=bucket, Key=file_name)
    file_data = response['Body'].read()

    return file_data


def decompress_backup(file_data):
    file_obj = io.BytesIO(file_data)
    files = {}
    tar_info = {}

    with tarfile.open(fileobj=file_obj, mode='r:gz') as tar:
        for member in tar.getmembers():
            if member.isfile():
                # Extract each member to a file-like object
                f = tar.extractfile(member)
                if f is not None:
                    # Read the content of the file-like object into a bytes object
                    content = f.read()
                    # Store the file data in the dictionary
                    files[member.name] = content
            elif member.isdir():
                # Store the directory in the dictionary with a value of None
                files[member.name] = None
            # Store the TarInfo object in the dictionary
            tar_info[member.name] = member

    return files, tar_info


def find_latest_game_profile(files, tar_info):
    latest_date = None
    latest_folder = None
    for file_name, file_content in files.items():
        # Get the TarInfo object for the file
        member = tar_info[file_name]

        if member.isdir():
            path_parts = member.name.split('/')

            if len(path_parts) == 3 and path_parts[1] == '0':
                # Update the latest folder if this folder was modified more recently
                if latest_date is None or member.mtime > latest_date:
                    latest_date = member.mtime
                    latest_folder = member.name

    latest_folder_name = os.path.basename(latest_folder)

    return latest_folder_name


def compress_backup(files, tar_info):
    tar_data = io.BytesIO()

    # Open the tarfile and add files
    with tarfile.open(fileobj=tar_data, mode='w:gz') as tar:
        for file_name, file_content in files.items():
            # Get the TarInfo object for the file
            info = tar_info[file_name]
            # Add the file to the tarball
            tar.addfile(info, io.BytesIO(file_content))

    # Seek back to the start of the BytesIO object
    tar_data.seek(0)

    return tar_data


def dump_backup(directory, files, tar_info):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for file_name, file_content in sorted(files.items()):
        info = tar_info[file_name]
        path = directory + file_name.lstrip('.')

        if info.isdir():
            os.makedirs(path, exist_ok=True)
        elif info.isfile():
            with open(path, 'wb') as f:
                f.write(file_content)


def get_player_guids(files, tar_info, game_profile):
    player_guids = []

    for file_name, file_content in files.items():
        # Get the TarInfo object for the file
        member = tar_info[file_name]

        if member.isfile():
            path_parts = member.name.split('/')

            if len(path_parts) == 5 and path_parts[2] == game_profile and path_parts[3] == 'Players':
                guid = path_parts[-1].split('.')[0]
                formatted_guid = guid[:8] + '-' + guid[8:12] + '-' + guid[12:16] + '-' + guid[16:20] + '-' + guid[20:]
                player_guids.append(formatted_guid.upper())

    return player_guids
