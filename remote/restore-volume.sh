#!/bin/bash

# Process named parameters
while (( "$#" )); do
  case "$1" in
    --volume)
      volume="$2"
      shift 2
      ;;
    --to-volume)
      to_volume="$2"
      shift 2
      ;;
    --from-volume)
      from_volume="$2"
      shift 2
      ;;
    --dump-name)
      dump_name="$2"
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
  if [ -z "${from_volume}" ]; then
    bad_migrate=true
  fi

  if [ -z "${to_volume}" ]; then
    bad_migrate=true
  fi

  if [ -n "${bad_migrate}" ]; then
    echo "Error: volume is a required parameter. Provide it as --volume=<value>." >&2
    exit 1
  fi
fi

if [ -n "${volume}" ]; then
  if [ -n "${from_volume}" ]; then
    bad_migrate=true
  fi

  if [ -n "${to_volume}" ]; then
    bad_migrate=true
  fi

  if [ -n "${bad_migrate}" ]; then
      echo "Error: must either use --volume or --from-volume and --to-volume" >&2
      exit 1
    fi
fi

volume="${volume:-${from_volume}}"
from_volume="${from_volume:-${volume}}"
to_volume="${to_volume:-${volume}}"

backupdir="./volume/${from_volume}/backup"

if [ -z "${dump_name}" ]; then
  dump_name="$(find "${backupdir}" -type f -exec basename {} \; | sort | tail -n 1)"
fi

if [[ ${dump_name: -7} != ".tar.gz" ]]; then
    dump_name="${dump_name}.tar.gz"
fi

docker run --rm --mount source="${to_volume}",destination=/data --mount type=bind,source="$(pwd)/${backupdir}",destination=/backup-dir cm2network/steamcmd:root bash -c "rm -rf /data/* && tar xvzf /backup-dir/${dump_name} -C /data . && chown -R steam:steam /data"