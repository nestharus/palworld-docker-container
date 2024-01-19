import os
import subprocess

# List of config files
config_files = ['config/docker.config', 'config/nginx.cong', 'config/palworld.config']

# Load environment variables from config files
for config_file in config_files:
    with open(config_file, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Run docker-compose build in root
subprocess.run(['docker-compose', 'build'], cwd='/')

# Get the Docker repository from environment variables
docker_repo = os.environ.get('DOCKER_REPO')

# List of images to push
images = ['nginx', 'palworld']

# Push each image to the Docker repository
for image in images:
    subprocess.run(['docker', 'push', f'{docker_repo}:{image}'])