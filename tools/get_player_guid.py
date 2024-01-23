import argparse
import shutil

from lib.backup import *
from lib.sav import *

parser = argparse.ArgumentParser(description="Fix snapshot of a Palworld server using older backup from S3")
parser.add_argument('--snapshot', type=str, required=True, help="Path to snapshot .tar.gz of Palworld Server")
parser.add_argument('--guild', type=str, required=True, help="Name of guild")
parser.add_argument('--name', type=str, required=True, help="Name of player")
args = parser.parse_args()

snapshot_files, snapshot_tar_info, game_profile = load_snapshot(args.snapshot)

temp_directory = './tmp'
snapshot_directory = f'{temp_directory}/snapshot'
os.makedirs(snapshot_directory, exist_ok=True)

dump_backup(snapshot_directory, snapshot_files, snapshot_tar_info)

world_to_json(snapshot_directory, game_profile)
snapshot_level_json = load_world_json(snapshot_directory, game_profile)
shutil.rmtree(temp_directory)

guilds = get_guilds(snapshot_level_json)
guids = [
    guid
    for guild in guilds
    for guid in get_player_guid(guild, args.guild, args.name)
]

if len(guids) == 0:
    print(f'Unable to find player {args.name} in guild {args.guild}')
    exit()

print(guids)