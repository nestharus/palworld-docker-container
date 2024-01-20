#!/bin/bash

# Process named parameters
while (( "$#" )); do
  case "$1" in
    --volume)
      to-volume="$2"
      shift 2
      ;;
    --to-volume)
      to-volume="$2"
      shift 2
      ;;
    --from-volume)
      from-volume="$2"
      shift 2
      ;;
    --dump-name)
      dump-name="$2"
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

if [ -z "${volume}" ]; then
  if [ -z "${from-volume}" ]; then
    bad_migrate=true
  fi

  if [ -z "${to-volume}" ]; then
    bad_migrate=true
  fi

  if [ -n "${bad_migrate}" ]; then
    echo "Error: volume is a required parameter. Provide it as --volume=<value>." >&2
    exit 1
  fi
fi

if [ -n "${volume}" ]; then
  if [ -n "${from-volume}" ]; then
    bad_migrate=true
  fi

  if [ -n "${to-volume}" ]; then
    bad_migrate=true
  fi

  if [ -n "${bad_migrate}" ]; then
      echo "Error: must either use --volume or --from-volume and --to-volume" >&2
      exit 1
    fi
fi

volume="${volume:-${from-volume}}"
from-volume="${from-volume:-${volume}}"
to-volume="${to-volume:-${volume}}"

backupdir="./volume/${from-volume}/backup"

if [ -z "${dump-name}" ]; then
  last_file_path=$(find "${backupdir}" -type f -exec basename {} \; | sort | tail -n 1)
  dump-name="$(basename "${last_file_path}")"
fi

docker run --rm -v "${volume}:/data" -v "${backupdir}:/backup-dir" ubuntu tar xvzf "/backup-dir/${dump-name}.tar.gz" -C /data