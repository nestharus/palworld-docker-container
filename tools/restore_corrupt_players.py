import glob
import boto3
import argparse
import shutil
from botocore.client import Config
from dotenv import load_dotenv

from lib.backup import *
from lib.sav import *

parser = argparse.ArgumentParser(description="Fix snapshot of a Palworld server using older backup from S3")
parser.add_argument('snapshot', type=str, help="Path to snapshot .tar.gz of Palworld Server")
parser.add_argument('backup', type=str, nargs='?', default=None, help="Backup directory")
args = parser.parse_args()

load_dotenv()

S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_HOST = 'https://' + os.getenv('S3_HOST')
S3_BUCKET = os.getenv('S3_BUCKET')
S3_VOLUME = os.getenv('S3_VOLUME')

s3 = None

if args.backup is None:
    # Initialize the S3 client
    s3 = boto3.client('s3',
        endpoint_url=S3_HOST,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

with open(args.snapshot, 'rb') as f:
    snapshot = f.read()
snapshot_files, snapshot_tar_info = decompress_backup(snapshot)
game_profile = find_latest_game_profile(snapshot_files, snapshot_tar_info)

temp_directory = './tmp'
snapshot_directory = f'{temp_directory}/snapshot'
backup_directory = f'{temp_directory}/backup'
os.makedirs(snapshot_directory, exist_ok=True)

dump_backup(snapshot_directory, snapshot_files, snapshot_tar_info)

player_guids = {*get_player_guids(snapshot_files, snapshot_tar_info, game_profile)}

print('Found .sav files for player guids')
print(player_guids)

world_to_json(snapshot_directory, game_profile)
snapshot_level_json = load_world_json(snapshot_directory, game_profile)

world_guids = get_world_guids(snapshot_level_json)
print('Found world guids for players')
print(world_guids.keys())

missing_player_guids = player_guids - world_guids.keys()

if len(missing_player_guids) == 0:
    print("No player guids to restore")
    shutil.rmtree('tmp')
    exit()

world_guids = {key: world_guids[key] for key in (missing_player_guids & world_guids.keys())}
restored_player_guids = {*()}

if s3 is None:
    file_list = os.listdir(args.backup)
    file_list = sorted(file_list, reverse=True)
else:
    file_list = fetch_backup_filenames(s3, S3_BUCKET, S3_VOLUME)

for file_name in file_list:
    print(f"Checking backup for restorations {file_name}")
    if s3 is None:
        with open(args.backup + '/' + file_name, 'rb') as file:
            backup_bytes = file.read()
    else:
        backup_bytes = fetch_backup(s3, S3_BUCKET, file_name)

    backup_snapshot_files, backup_snapshot_tar_info = decompress_backup(backup_bytes)

    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

    backup_guids = {*get_player_guids(backup_snapshot_files, backup_snapshot_tar_info, game_profile)}
    restore_backup_guids = backup_guids & missing_player_guids

    if len(restore_backup_guids) == 0:
        print(f"Backup is too old {file_name}")
        break

    dump_backup(backup_directory, backup_snapshot_files, backup_snapshot_tar_info)

    world_to_json(backup_directory, game_profile)
    backup_level_json = load_world_json(backup_directory, game_profile)
    backup_world_guids = get_world_guids(backup_level_json)
    backup_world_guids = {key: backup_world_guids[key] for key in (missing_player_guids & backup_world_guids.keys())}

    if len(backup_world_guids) == 0:
        print(f"No restorable world guids found in backup {file_name}")
        continue

    restored_player_guids.update(backup_world_guids.keys())
    missing_player_guids = missing_player_guids - backup_world_guids.keys()

    for backup_guid, backup_record in backup_world_guids.items():
        print(f'Restoring player {backup_guid}')

        shutil.copy(
            f'{backup_directory}/0/{game_profile}/Players/{backup_guid.replace("-", "")}.sav',
            f'{snapshot_directory}/0/{game_profile}/Players/{backup_guid.replace("-", "")}.sav'
        )

        world_guids[backup_guid] = backup_record

    shutil.rmtree(backup_directory)

    if len(missing_player_guids) == 0:
        break

if len(missing_player_guids) != 0:
    print("Unable to restore player guids")
    print(missing_player_guids)

if len(restored_player_guids) == 0:
    print("No player guids restored")
    shutil.rmtree('tmp')
    exit()

print("Successfully restored player guids")
print(restored_player_guids)

patch_world_guid(snapshot_level_json, world_guids)
world_to_sav(snapshot_directory, game_profile)

for file in glob.glob(f'{snapshot_directory}/0/{game_profile}/Players/*.json'):
    os.remove(file)

for file in glob.glob(f'{snapshot_directory}/0/{game_profile}/*.json'):
    os.remove(file)

tarball = compress_backup(snapshot_files, snapshot_tar_info)
base_filename = os.path.basename(args.snapshot)
name, ext = os.path.splitext(base_filename)
new_filename = name + ".restored" + ext
dir_name = os.path.dirname(args.snapshot)
new_filepath = os.path.join(dir_name, new_filename)

with open(new_filepath, 'wb') as f:
    f.write(tarball.read())

shutil.rmtree('tmp')
