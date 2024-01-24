# restore_corrupt_players.py
This is used to repair infinite loading screen and any arbitrary bugs.
The script has two functions. Only one function can operate at a time.
1. Rollback individual players
2. Readd players to Level.sav

### Arguments
1. --snapshot
   - .tar.gz
       - tree format ./0/...
       - --snapshot ./SNAPSHOT_NAME.tar.gz
   - S3 path to .tar.gz
     - tree format ./0/...
     - requires editing .env file
     - --snapshot https://host/palworld/PALWORLD_DATA/SNAPSHOT_NAME.tar.gz
   - folder path
     - SNAPSHOT_NAME/0/... 
     - --snapshot SNAPSHOT_NAME
2. --backup
   - The location of backups. This is a folder with multiple backups inside of it!!
   - The backups must be named by timestamps when they were taken
   - The script loads backups from the most recent to the oldest and depends on the names!
   - If this argument is not provided backups will automatically be used from S3 instead
   - The backup parameter can point to S3 or a local folder
   - The data within a local folder can be .tar.gz archives or folders
   - --backup ./MY_BACKUPS
     - ./MY_BACKUPS/20240122050001.tar.gz
     - ./MY_BACKUPS/20240122050001/0/...
   - --backup https://host/palworld/PALWORLD_DATA
     - https://host/palworld/PALWORLD_DATA/20240122050001.tar.gz
   - .tar.gz
       - tree format ./0/...
       - --backup ./SNAPSHOT_NAME.tar.gz
   - S3 path to .tar.gz
       - tree format ./0/...
       - requires editing .env file
   - folder path
       - SNAPSHOT_NAME/0/...
3. --profile
   - The folders directly under 0 are the profile ids that can be used here
   - This is not needed if your snapshot only has 1 profile
   - If your snapshot has more than 1 profile then you must specify it with this argument
   - --profile 87BACF20D22B4A3AAD87215350937C66
4. --guids
   - A comma separated list of guid ids to patch from a specific backup for the purpose of an individual rollback.
   - --guids 5E33C52B000000000000000000000000,7106424B000000000000000000000000
   - --guids C758100E-0000-0000-0000-000000000000,5E33C52B-0000-0000-0000-000000000000

# get_player_guid.py
This is used to find the guid of a player given a guild name and a player name.

1. --snapshot
   - .tar.gz
       - tree format ./0/...
       - --snapshot ./SNAPSHOT_NAME.tar.gz
   - S3 path to .tar.gz
     - tree format ./0/...
     - requires editing .env file
     - --snapshot https://host/palworld/PALWORLD_DATA/SNAPSHOT_NAME.tar.gz
   - folder path
     - SNAPSHOT_NAME/0/... 
     - --snapshot SNAPSHOT_NAME
2. --profile
   - The folders directly under 0 are the profile ids that can be used here
   - This is not needed if your snapshot only has 1 profile
   - If your snapshot has more than 1 profile then you must specify it with this argument
   - --profile 87BACF20D22B4A3AAD87215350937C66
3. --guild
   - The name of the in-game guild that the player belongs to
   - Guildless players belong to the Unnamed Guild
   - -- guild "Unnamed Guild"
4. --name
   - The in-game name of the player to find the guid for
   - --name "I'm a player"