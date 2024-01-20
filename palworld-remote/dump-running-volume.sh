#!/bin/bash

# Process named parameters
while (( "$#" )); do
  case "$1" in
    --container)
      container="$2"
      shift 2
      ;;
    --volume)
      volume="$2"
      shift 2
      ;;
    --mount)
      mount="$2"
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

if [ -z "$container" ]; then
  echo "Error: container is a required parameter. Provide it as --container=<value>." >&2
  missing_parameters=true
fi

if [ -z "$mount" ]; then
  echo "Error: mount is a required parameter. Provide it as --mount=<value>." >&2
  missing_parameters=true
fi

if [ -z "$volume" ]; then
  echo "Error: volume is a required parameter. Provide it as --volume=<value>." >&2
  missing_parameters=true
fi

if [ "$missing_parameters" = true ]; then
  exit 1
fi

backupdir="./volume/${volume}/backup"
tempdir="./volume/${volume}/temp"
timestamp=$(date +%Y%m%d%H%M%S)

# Create the dump directory
mkdir -p "${backupdir}"

containerId=$(docker ps -qf "name=${container}")

# Copy data from the volumes to the host
mkdir -p "${tempdir}"

docker cp "${containerId}:${mount}" "${tempdir}"

folder=$(basename "${mount}")

tar cvzf "${backupdir}/${timestamp}.tar.gz" -C "${tempdir}/${folder}" .

rm -rf "${tempdir}"