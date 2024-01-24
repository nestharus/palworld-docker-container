import argparse

from dotenv import load_dotenv
from lib.save_archive.factory import save_archive_factory
from lib.main_utils import find_game_profile
from lib.save_archive.utils import get_game_profile_folder, get_level_file
from lib.sav.gvas import decompress_gvas
from lib.sav.uesave import gvas_to_json
from lib.sav.sav import get_guilds, get_player_guid

parser = argparse.ArgumentParser(description="Fix snapshot of a Palworld server using older backup from S3")
parser.add_argument('--snapshot', type=str, required=True, help="Path to snapshot of Palworld Server: .tar.gz (./0/...), S3 .tar.gz (./0/...), or folder (SNAPSHOT_NAME/0/...)")
parser.add_argument('--profile', type=str, default=None, help="Game profile to use (/0/profileid)")
parser.add_argument('--guild', type=str, required=True, help="Name of guild")
parser.add_argument('--name', type=str, required=True, help="Name of player")
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

print(f'Loading snapshot level')
snapshot_level_name = get_level_file(snapshot, snapshot_game_profile_folder)
snapshot_level_gvas, snapshot_level_gvas_type = decompress_gvas(snapshot[snapshot_level_name])
snapshot_level_json = gvas_to_json(snapshot_level_gvas)

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
