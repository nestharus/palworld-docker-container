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
2. copy config files to server
3. `set -a; . ./docker.config; set +a`
4. `set -a; . ./nginx.config; set +a`
5. `set -a; . ./palworld.config; set +a`
6. `docker-compose up`

# Configuring Nginx
- If you do not want the server to be listed then the 25575 server block can be removed.