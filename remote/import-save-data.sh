#!/bin/bash

source ./config/docker.config
source ./config/nginx.config
source ./config/palworld.config

# Create a temporary container that mounts the volume
docker run --rm -d -v "$(basename $(pwd))_PALWORLD_DATA:/volume" --name temp-container alpine sh -c "tail -f /dev/null"

# Copy data from the host to the volume
docker cp "${PALWORLD_SAVE_DATA}/." temp-container:/volume

# Stop and remove the temporary container
docker stop temp-container