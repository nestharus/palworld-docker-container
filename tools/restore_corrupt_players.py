import glob
import boto3
import argparse
import shutil
from botocore.client import Config
from dotenv import load_dotenv

from lib.backup import *
from lib.sav import *

parser = argparse.ArgumentParser(description="Fix snapshot of a Palworld server using older backup from S3")
parser.add_argument('--snapshot', type=str, required=True, help="Path to snapshot .tar.gz of Palworld Server")
parser.add_argument('--backup', type=str, default=None, help="Backup directory")
parser.add_argument('--guids', type=str, default=None, help="Comma separated list of guids to restore")
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

snapshot_files, snapshot_tar_info, game_profile = load_snapshot(args.snapshot)

temp_directory = './tmp'
snapshot_directory = f'{temp_directory}/snapshot'
backup_directory = f'{temp_directory}/backup'
os.makedirs(snapshot_directory, exist_ok=True)

dump_backup(snapshot_directory, snapshot_files, snapshot_tar_info)

player_guids = {*get_player_guids(snapshot_files, snapshot_tar_info, game_profile)}

world_to_json(snapshot_directory, game_profile)
snapshot_level_json = load_world_json(snapshot_directory, game_profile)
os.remove(f'{snapshot_directory}/0/{game_profile}/Level.sav.json')
os.remove(f'{snapshot_directory}/0/{game_profile}/Level.sav.gvas')
print(f"World Guid Count {len(get_world_guids(snapshot_level_json))}")
world_guids = get_world_guids(snapshot_level_json)

if args.guids is None:
    missing_player_guids = player_guids - world_guids.keys()
else:
    missing_player_guids = {*args.guids.split(',')}

if len(missing_player_guids) == 0:
    print("No player guids to restore")
    shutil.rmtree('tmp')
    exit()

print("Missing player guids")
print(missing_player_guids)

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
    backup_level_json = None
    backup_world_guids = {key: backup_world_guids[key] for key in (missing_player_guids & backup_world_guids.keys())}

    if len(backup_world_guids) == 0:
        print(f"No restorable world guids found in backup {file_name}")
        continue

    backup_world_guids_to_patch = {key: backup_world_guids[key] for key in (world_guids & backup_world_guids.keys())}
    backup_world_guids_to_add = {key: backup_world_guids[key] for key in (backup_world_guids.keys() - backup_world_guids_to_patch.keys())}

    restored_player_guids.update(backup_world_guids.keys())
    missing_player_guids = missing_player_guids - backup_world_guids.keys()

    if len(backup_world_guids_to_add) > 0:
        print(f'Adding world guids {backup_world_guids_to_add.keys()}')
        get_world_records(snapshot_level_json).extend(backup_world_guids_to_add.values())

    if len(backup_world_guids_to_patch) > 0:
        print(f'Patching world guids {backup_world_guids_to_patch.keys()}')
        world_records = get_world_records(snapshot_level_json)
        for i, world_record in enumerate(world_records):
            world_record_guid = get_world_record_guid(world_record)
            if world_record_guid in backup_world_guids_to_patch:
                print(f'Patching player into world {world_record_guid}')
                world_records[i] = backup_world_guids[world_record_guid]

    for backup_guid, backup_record in backup_world_guids.items():
        print(f'Restoring player .sav {backup_guid}')

        shutil.copy(
            f'{backup_directory}/0/{game_profile}/Players/{backup_guid.replace("-", "")}.sav',
            f'{snapshot_directory}/0/{game_profile}/Players/{backup_guid.replace("-", "")}.sav'
        )

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

print(f"World Guid Count {len(get_world_guids(snapshot_level_json))}")

print("Successfully restored player guids")
print(restored_player_guids)

save_world_json(snapshot_directory, game_profile, snapshot_level_json)
snapshot_level_json = None
world_to_sav(snapshot_directory, game_profile)
os.remove(f'{snapshot_directory}/0/{game_profile}/Level.sav.json')
os.remove(f'{snapshot_directory}/0/{game_profile}/Level.sav.gvas')

base_filename = os.path.basename(args.snapshot)
name, gz = os.path.splitext(base_filename)
name, tar = os.path.splitext(name)
new_filename = name + ".restored" + tar + gz
dir_name = os.path.dirname(args.snapshot)
new_filepath = os.path.join(dir_name, new_filename)

with tarfile.open(new_filepath, 'w:gz') as tar:
    full_path = os.path.abspath(snapshot_directory)
    relative_path = os.path.relpath(full_path, snapshot_directory)
    tar.add(full_path, arcname='./')

shutil.rmtree(temp_directory)
