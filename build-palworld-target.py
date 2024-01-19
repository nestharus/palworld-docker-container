import os
import subprocess
from time import sleep

# List of config files
config_files = ['config/docker.config', 'config/nginx.cong', 'config/palworld.config']

# Load environment variables from config files
for config_file in config_files:
    with open(config_file, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Run docker-compose up -d
subprocess.run(['docker-compose', 'up', '-d', 'palworld-target'], cwd='palworld-target')