#!/bin/bash

volume=${1:-}

# Process named parameters
while (( "$#" )); do
  case "$1" in
    --volume)
      volume="$2"
      shift 2
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

# Check if app is set
if [ -z "$volume" ]; then
  echo "Error: volume is a required parameter. Provide it as the first positional argument or as --volume=<value>." >&2
  exit 1
fi

backupdir="./volume/${volume}/backup"
tempdir="./volume/${volume}/temp"
timestamp=$(date +%Y%m%d%H%M%S)

# Create the dump directory
mkdir -p "${backupdir}"

containerId=$(docker run -d --rm --mount source="${volume}",destination=/data ubuntu sleep infinity)

docker exec "$containerId" bash -c "cd /data && tar -czf ../data.tar.gz ."
docker cp "$containerId:/data.tar.gz" "$backupdir/$timestamp.tar.gz"

docker stop "${containerId}"