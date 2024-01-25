import argparse

from dotenv import load_dotenv

from lib.save_archive.utils import *
from lib.main_utils import *
from lib.sav.gvas import *
from lib.sav.uesave import *
from lib.sav.sav import *

parser = argparse.ArgumentParser(description="NA")
parser.add_argument('--snapshot', type=str, required=True, help="Path to snapshot")
parser.add_argument('--backup', type=str, default=None, help="Path to directory with backups")
parser.add_argument('--profile', type=str, default=None, help="Game profile to use")
parser.add_argument('--guids', type=str, default=None, help="Comma separated list of guids")
args = parser.parse_args()

load_dotenv()

snapshot_archive = save_archive_factory(args.snapshot)
snapshot = snapshot_archive.load()

print(f'Loaded snapshot {args.snapshot}')

game_profile = find_game_profile(snapshot, args.profile)

if game_profile is None:
    exit()

print(f'Using game profile: {game_profile}')

snapshot_game_profile_folder = get_game_profile_folder(snapshot, game_profile)
snapshot_guids = {*get_player_guids(snapshot, snapshot_game_profile_folder)}

if len(snapshot_guids) == 0:
    print(f'No player guids to restore')
    exit()

print(f'Loading snapshot level')
snapshot_level_name = get_level_file(snapshot, snapshot_game_profile_folder)
snapshot_level_gvas, snapshot_level_gvas_type = decompress_gvas(snapshot[snapshot_level_name])
snapshot_level_json = gvas_to_json(snapshot_level_gvas)

snapshot_world_guids = get_world_guids(snapshot_level_json)

if args.guids is None:
    missing_player_guids = snapshot_guids - snapshot_world_guids.keys()
else:
    missing_player_guids = {*args.guids.split(',')}
    missing_player_guids = {
        guid[:8] + '-' + guid[8:12] + '-' + guid[12:16] + '-' + guid[16:20] + '-' + guid[20:]
        for guid in missing_player_guids
        if '-' not in guid
    }


if len(missing_player_guids) == 0:
    print("No player guids to restore")
    exit()

print("Missing player guids")
print(missing_player_guids)

restored_player_guids = {*()}

backup_repo = get_backup_repo(args.backup)
backup_names = backup_repo.list()

for backup_name in backup_names:
    print(f'Loading backup {backup_name}')

    backup_archive = backup_repo.load(backup_name)
    backup = backup_archive.archive

    backup_game_profile_folder = get_game_profile_folder(backup, game_profile)

    if backup_game_profile_folder is None:
        print(f'Backup {backup_name} is too old to restore {game_profile}')
        break

    print(f'Game Profile: {game_profile}')

    backup_player_guids = {*get_player_guids(backup, backup_game_profile_folder)}
    backup_player_guids = backup_player_guids & missing_player_guids

    if len(backup_player_guids) == 0:
        print(f"Backup is too old {backup_name}")
        break

    print(f'Loading backup level')
    backup_level_name = get_level_file(backup, backup_game_profile_folder)
    backup_level_gvas, _ = decompress_gvas(backup[backup_level_name])
    backup_level_json = gvas_to_json(backup_level_gvas)

    backup_world_guids = get_world_guids(backup_level_json)
    backup_world_guids = {key: backup_world_guids[key] for key in (missing_player_guids & backup_world_guids.keys())}

    if len(backup_world_guids) == 0:
        print(f"No restorable world guids found in backup {backup_name}")
        continue

    backup_world_guids_to_patch = {key: backup_world_guids[key] for key in (snapshot_world_guids & backup_world_guids.keys())}
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

    for backup_guid in backup_world_guids.keys():
        print(f'Restoring player .sav {backup_guid}')

        backup_player_file = get_player_file(backup, backup_game_profile_folder, backup_guid)
        snapshot_player_file = get_player_file(snapshot, snapshot_game_profile_folder, backup_guid)

        print(f'Writing backup.{backup_player_file} to snapshot.{snapshot_player_file}')
        snapshot[snapshot_player_file] = backup[backup_player_file]

    if len(missing_player_guids) == 0:
        break

if len(missing_player_guids) != 0:
    print("Unable to restore player guids")
    print(missing_player_guids)

if len(restored_player_guids) == 0:
    print("No player guids restored")
    shutil.rmtree('tmp')
    exit()

print('Successfully restored player guids')
print(restored_player_guids)

print(f'Saving snapshot level to snapshot.{snapshot_level_name}')
snapshot_level_gvas = json_to_gvas(snapshot_level_json)
snapshot[snapshot_level_name] = compress_gvas(snapshot_level_gvas, snapshot_level_gvas_type)

print(f'Saving snapshot as {snapshot_archive.path}.restored')
snapshot_archive.save_as(path=f'{snapshot_archive.path}.restored')
