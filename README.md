# Configure Config Files In /config

# DOWNLOAD PALWORLD SERVER FILES
1. `cd palworld-downloader`
2. `mkdir downloaded`
3. `docker-compose up`

# UPDATE PALWORLD SERVER
1. `cd palworld
2. `docker-compose build`

# DEPLOY PALWORLD SERVER
1. `pipenv install`
2. cd palworld
3. modify .env REPOSITORY
4. pipenv run py push.py

# RUN SERVER
1. copy palworld-remote to server
2. `docker-compose up -d`

# STOP SERVER
1. `docker-compose down`

# BACKUP SERVER WHILE RUNNING
1. `./dump-running-volume.sh --container=palworld --volume=$(basename "$(pwd)")_PALWORLD_DATA --mount=/palworld/Pal/Saved/SaveGames`

# BACKUP VOLUME
1. `./dump-volume.sh --volume=$(basename "$(pwd)")_PALWORLD_DATA`

# RESTORE VOLUME
1. `./restore-volume.sh --volume=$(basename "$(pwd)")_PALWORLD_DATA`

# RESTORE VOLUME TO NEW NAME
1. `./restore-volume.sh --from-volume=$(basename "$(pwd)")_PALWORLD_DATA --to-volume=<NEW_NAME>`

# ROLLBACK VOLUME
1. `./restore-volume.sh --volume=$(basename "$(pwd)")_PALWORLD_DATA --dump-name=<FILENAME>`