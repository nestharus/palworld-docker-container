# UPDATE PALWORLD SERVER
1. `cd /target`
2. `docker-compose up -d`
3. wait awhile for initialization
4. `docker-compose down`
5. modify /target/app files

# DEPLOY IMAGES
1. `docker-compose build -e PALWORLD_ROUTE=route -e DOCKER_REPO=repo`
2. `docker push repo:nginx`
3. `docker push repo:palworld`

# RUN SERVER
1. copy remote/docker-compose.yml to server
2. From server `docker-compose up -e PALWORLD_PLAYERS=32`

# Configuring Nginx
- If you do not want the server to be listed then the 25575 server block can be removed.