import os
import shutil
import tarfile
import datetime
import argparse
import subprocess

# Process named parameters
parser = argparse.ArgumentParser()
parser.add_argument('--container', required=True)
parser.add_argument('--volume', required=True)
parser.add_argument('--mount', required=True)
args = parser.parse_args()

backupdir = f"./volume/{args.volume}/backup"
tempdir = f"./volume/{args.volume}/temp"
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Create the dump directory
os.makedirs(backupdir, exist_ok=True)

# Get container ID
container_id = subprocess.check_output(['docker', 'ps', '-qf', f'name={args.container}']).decode().strip()

# Copy data from the volumes to the host
os.makedirs(tempdir, exist_ok=True)
subprocess.run(['docker', 'cp', f'{container_id}:{args.mount}', tempdir], check=True)

# Create a tar file
with tarfile.open(f'{backupdir}/{timestamp}.tar.gz', 'w:gz') as tar:
    tar.add(tempdir, arcname='')

# Remove the temp directory
shutil.rmtree(tempdir)