### Download/Update The Server Files From Steam
1. `cd downloader`
2. `mkdir downloaded`
3. `docker-compose up`

### Update Your Palworld Image That The Server Will Use
1. `docker-compose build`

### Deploy Palworld Server Image So That Your Server Can Use It!
1. modify .env REPOSITORY to point to your docker repo
    - It points to my docker repo by default and you can't push to my repo grr
2. pipenv run py push.py

