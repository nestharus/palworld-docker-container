#!/bin/bash

echo "Initializing Root Configuration"

CONFIG_FILEPATH="/palworld/Pal/Saved/Config/LinuxServer"

mkdir -p "${CONFIG_FILEPATH}"
chown steam:steam "${CONFIG_FILEPATH}"