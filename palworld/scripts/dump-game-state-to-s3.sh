#!/bin/bash

echo "Snapshotting Game State"

if [ ! -d "/palworld/Pal/Saved/SaveGames" ]; then
    echo "Unable To Snapshot. No Game State Profile Present"
    exit 0
fi

if [ ! "$(ls -A /palworld/Pal/Saved/SaveGames)" ]; then
    echo "Unable To Snapshot. No Game State Profile Present"
    exit 0
fi

if [ ! "$(ls -A /palworld/Pal/Saved/SaveGames/0)" ]; then
    echo "Unable To Snapshot. No Game State Profile Present"
    exit 0
fi

timestamp=$(date +%Y%m%d%H%M%S)

# Create the dump directory
mkdir -p "/tmp/palworld"

folder_name="/palworld/Pal/Saved/SaveGames"

echo "Snapshotting Game State Profile: ${folder_name}"

# Create a tar file from the folder
tar -czf /tmp/palworld/${timestamp}.tar.gz -C "$folder_name" .

# Upload the tar file to the S3 bucket
s3cmd put /tmp/palworld/${timestamp}.tar.gz s3://${S3_BUCKET}/${PUBLIC_IP}/${S3_VOLUME}/

# Remove the tar file
rm /tmp/palworld/${timestamp}.tar.gz

echo "Snapshot Game State Successful"