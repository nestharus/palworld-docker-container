# Personal Machine Tools For Maintaining Images!
### Prepare Your Machine For The Tools
1. https://www.pythontutorial.net/python-basics/install-pipenv-windows/
2. https://docs.docker.com/desktop/install/windows-install/
3. From root of this project
   - `pipenv install`

### Download/Update The Server Files From Steam
1. `cd palworld-downloader`
2. `mkdir downloaded`
3. `docker-compose up`

### Update Your Palworld Image That The Server Will Use
1. `cd palworld
2. `docker-compose build`

### Deploy Palworld Server Image So That Your Server Can Use It!
1. cd palworld
2. modify .env REPOSITORY to point to your docker repo
   - It points to my docker repo by default and you can't push to my repo grr
3. pipenv run py push.py

### Mods/Plugins
1. From palworld-modded directory
2. Modify .env VANILLA_REPOSITORY to point to vanilla server file image
3. Modify .env MODDED_REPOSITORY to point to modded server file image that you will deploy
4. Modify Dockerfile to copy mods/plugins
5. pipenv run py push.py
6. You will be using this image instead of the vanilla one in your server docker-compose.yml if you want mods and plugins

# From Your Server! It's Time To Rock!!
### Prepare Your Server For Awesomeness
1. After your server is deployed it should have docker and sftp on it
2. vps-bootstrap/bootstrap.sh is a script that will install everything necessary
   - ssh into your server
   - copy bootstrap.sh line by line into your server and execute
3. Download filezilla
4. Connect to your server sftp://IP_ADDRESS

### Configuring Your Settings
1. Edit the palworld-remote/palworld/env/.override.env file
    - Copy settings from .default.env to .override.env and then edit
    - PUBLIC_IP is important! It should be the ip address of your server
    - S3 BACKUP uses PUBLIC_IP as part of the path for backups
2. Edit the palworld-remote/docker-compose.yml file
    - You are specifically editing which presets you want to use
    - Comment out/in presets you want/don't want
3. Edit palworld-remote/.env file
   - This file should point to your docker repo if you are maintaining your own image

### Run Your Server From The Image!!
1. copy palworld-remote to server
2. If this is your first run and you have no data `docker volume create PALWORLD_DATA`
3. From palworld-remote folder `docker-compose up -d`

### Where are my backup archives???
1. In S3 under the palworld bucket organized by server IP Address
2. The filenames are named after timestamps like 20240121194618
   - 2024 is the year
   - 01 is the month
   - 21 is the day
   - 19 is the hour
   - 46 is the minute
   - 18 is the second
3. Download that archive and get ready to put it into your server!

### How do I get my data archive from a random server that isn't on this??
1. You'll need to tarball your /Pal/Saved/SaveGames folder
2. The root of your tarball should be the 0 directory!
3. If you are converting a local save to a server save here is how to include the host's player data
   - https://github.com/xNul/palworld-host-save-fix
4. If you have jolly corruption here is a tool to convert to .sav files to json and back so you can edit them
   - https://gist.github.com/arawrshi/4a65a9aba62910f531d08e3b82e2fcdf

### How To Get Your Data Archive Into The Server For Backup
1. From your palworld-remote folder
2. Create volume directory if it does not exist
3. From palworld-remote/volume
4. Create PALWORLD_DATA directory if it does not exist
5. From palworld-remote/volume/PALWORLD_DATA
6. Create backup directory if it does not exist
7. From palworld-remote/volume/PALWORLD_DATA/backup
8. Copy your .tar.gz file
    - It should have a name like this 20240121194618.tar.gz
9. From palworld-remote folder
10. You can now run `./restore-volume.sh --volume PALWORLD_DATA --dump-name <TAR_GZ_FILENAME>`
11. After you start your server it will have the data from the archive you imported

### Stop Palworld Server
1. From palworld-remote folder `docker-compose down`

### Backup Palworld Server While Running
1. From palworld-remote folder `./dump-running-volume.sh --container palworld --volume PALWORLD_DATA --mount /palworld/Pal/Saved/SaveGames`
    - Edit file permissions in filezilla to have execute permission!

### Backup Palworld Server Volume
1. From palworld-remote folder `./dump-volume.sh --volume PALWORLD_DATA`
    - Edit file permissions in filezilla to have execute permission!

### Restore Volume
1. From palworld-remote folder `./restore-volume.sh --volume PALWORLD_DATA`
    - Edit file permissions in filezilla to have execute permission!

### Restore Volume To New Name
1. From palworld-remote folder `./restore-volume.sh --from-volume PALWORLD_DATA --to-volume <NEW_NAME>`
    - Edit file permissions in filezilla to have execute permission!

### Rollback Volume
1. From palworld-remote folder `./restore-volume.sh --volume PALWORLD_DATA --dump-name <FILENAME>`
    - Edit file permissions in filezilla to have execute permission!

### Display Volume
1. From palworld-remote folder `./display-volume.sh PALWORLD_DATA`
    - Edit file permissions in filezilla to have execute permission!

# Player Troubleshooting

### Infinite Loading Screen

This currently checks for the missing player variant of the infinite loading screen.
It may not detect the wiped player variant. A wiped player may still be in Level.sav.

1. Go to tools
2. Modify .env file
3. Shut down your server
4. Snapshot server with `./dump-volume.sh --volume PALWORLD_DATA`
5. Download snapshot archive
6. `pipenv run py ./restore_corrupt_players.py PATH_TO_SNAPSHOT_ARCHIVE`
7. A restored archive will be created in the same directory as the snapshot archive
8. Upload restored archive to server ./volume/PALWORLD_DATA/backup
9. `./restore-volume.sh --volume PALWORLD_DATA --dump-name RESTORED_ARCHIVE_NAME`
   - Don't include the .tar.gz extension in the name for dump-name parameter

If you want to minimize server downtime you can identify the required backups beforehand
and save them locally. When running restore_corrupt_players.py
- `pipenv run py ./restore_corrupt_players.py PATH_TO_SNAPSHOT_ARCHIVE ./backup`

### Individual Player Rollback For All Other Issues

1. If a player is bugged for whatever reason they can be rolled back
   - You will need to know what time to roll the player back to!
   - You will need to know the player's guild and name
   - Guildless players are in Unnamed Guild
2. Shut down your server
3. Snapshot server with `./dump-volume.sh --volume PALWORLD_DATA`
4. Download snapshot archive
5. Download archive you will be rolling player back to
6. `pipenv run get_player_guid.py --snapshot "PATH_TO_BACKUP" --guild "GUILD_NAME" --name PLAYER_NAME`
7. `pipenv run py ./restore_corrupt_players.py "PATH_TO_SNAPSHOT_ARCHIVE" --backup "PATH_TO_BACKUP_ARCHIVE --guids COMMA_SEPARATED_LIST_OF_GUIDS_TO_ROLLBACK`
8. A restored archive will be created in the same directory as the snapshot archive
9. Upload restored archive to server ./volume/PALWORLD_DATA/backup
10. `./restore-volume.sh --volume PALWORLD_DATA --dump-name RESTORED_ARCHIVE_NAME`
   - Don't include the .tar.gz extension in the name for dump-name parameter