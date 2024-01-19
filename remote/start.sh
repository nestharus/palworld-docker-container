#!/bin/bash

source ./config/docker.config
source ./config/nginx.config
source ./config/palworld.config

docker stop $(docker ps -qa) && docker system prune -af
docker compose down
docker compose build --no-cache
docker compose up