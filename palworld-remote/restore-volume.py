import os
import argparse
import subprocess
import shutil

# Process named parameters
parser = argparse.ArgumentParser()
parser.add_argument('--volume')
parser.add_argument('--to-volume')
parser.add_argument('--from-volume')
parser.add_argument('--dump-name')
args = parser.parse_args()

volume = args.volume or args.from_volume
from_volume = args.from_volume or volume
to_volume = args.to_volume or volume

if not volume or not from_volume or not to_volume:
    print("Error: volume is a required parameter. Provide it as --volume=<value>.")
    exit(1)

backupdir = f"./volume/{from_volume}/backup"

if not args.dump_name:
    # Get the last file in the backup directory
    files = [f for f in os.listdir(backupdir) if os.path.isfile(os.path.join(backupdir, f))]
    files.sort()
    dump_name = files[-1]
else:
    dump_name = args.dump_name

# Run the docker command
subprocess.run(['docker', 'run', '--rm', '-v', f'{volume}:/data', '-v', f'{backupdir}:/backup-dir', 'ubuntu', 'tar', 'xvzf', f'/backup-dir/{dump_name}', '-C', '/data'], check=True)