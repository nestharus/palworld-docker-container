#!/bin/bash

source ./config/docker.config
source ./config/nginx.config
source ./config/palworld.config

# Get the timestamp
timestamp=$(date +%Y%m%d%H%M%S)

# Create the dump directory
mkdir -p ./palworld/dump/$timestamp

# Get the container ID of the running palworld service
containerId=$(docker ps -qf "name=palworld")

# Copy data from the volumes to the host
docker cp $containerId:/app/Pal/Saved/SaveGames ./palworld/dump/$timestamp/savegames
docker cp $containerId:/app/Pal/Saved/Config ./palworld/dump/$timestamp/config