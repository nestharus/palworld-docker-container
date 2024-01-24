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