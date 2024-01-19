# Configure Config Files In /config

# UPDATE PALWORLD SERVER
1. `pipenv install`
2. `pipenv run python build-palworld-target.py`
3. wait awhile for initialization
4. `docker-compose down -d palworld-target`
5. modify /target/app files

# DEPLOY IMAGES
1. `pipenv run python build-and-deploy.py`

# RUN SERVER
1. copy remote/docker-compose.yml to server
2. copy remove/start.sh to server
3. copy config files to server
4. copy palworld/config to server
5. `./start.sh`

---------------------
`source ./env.sh`