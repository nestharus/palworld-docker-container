import os
import subprocess

# List of config files
config_files = ['config/docker.config', 'config/nginx.config', 'config/palworld.config']

# Load environment variables from config files
for config_file in config_files:
    with open(config_file, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Run docker-compose build in the correct directory
result = subprocess.run(['docker-compose', 'build'])

# Check if the build was successful
if result.returncode != 0:
    print('docker-compose build failed with return code', result.returncode)
    exit(1)

# Get the Docker repository from environment variables
docker_repo = os.environ.get('DOCKER_REPO')

# List of images to push
images = ['nginx', 'palworld']

# Push each image to the Docker repository
for image in images:
    result = subprocess.run(['docker', 'push', f'{docker_repo}:{image}'])

    # Check if the push was successful
    if result.returncode != 0:
        print(f'Failed to push image {docker_repo}:{image} with return code', result.returncode)