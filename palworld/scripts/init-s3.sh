#!/bin/bash

# Check if S3 backup is enabled
if [ "$ENABLE_S3_BACKUP" = "false" ]
then
    echo "Warning: S3 Backup Is Disabled!"
    exit 0
fi

echo "S3 Backup Is Enabled"

# Write .s3cfg file
cat << EOF > ~/.s3cfg
[default]
access_key = ${S3_ACCESS_KEY}
secret_key = ${S3_SECRET_KEY}
host_base = ${S3_HOST}
host_bucket = %(bucket)s.${S3_HOST}
EOF

echo ".s3cfg file has been written to the home directory."

if ! s3cmd ls "s3://${S3_BUCKET}" > /dev/null 2>&1 ; then
    echo "S3 Bucket Does Not Exist, Creating It."
    s3cmd mb "s3://${S3_BUCKET}"
fi

script_dir=$(dirname $(realpath $0))
script_path="${script_dir}/dump-game-state-to-s3.sh"

if crontab -l | grep -q "${script_path}"; then
    # Cron job exists, do nothing
    echo "Backup cron job already exists, doing nothing."
else
    # Cron job does not exist, add it to the crontab
    echo "Backup cron job does not exist, adding it."
    (crontab -l ; echo "${S3_BACKUP_PERIOD} S3_BUCKET=${S3_BUCKET} PUBLIC_IP=${PUBLIC_IP} S3_VOLUME=${S3_VOLUME} ${script_path}") | crontab -
fi

./scripts/dump-game-state-to-s3.sh

cron