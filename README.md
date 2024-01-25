### Prepare Your Machine For Running Locally
1. Go to the microsoft store and download Windows Subsystem for Linux
2. Go to windows features
3. Turn on Virtual Machine Platform
4. Turn On Windows Subsystem for Linux
5. Restart
6. https://www.pythontutorial.net/python-basics/install-pipenv-windows/
7. https://docs.docker.com/desktop/install/windows-install/
8. From root of this project
   - `pipenv install`

### Image Folder
Used to build the docker image from steam server files. Only useful if you plan to maintain your own docker image.

### Modded Folder
Used to include mods for your server.
You will need to build this image and push it to your own docker repo.
See .env file. Run push.py to build and push images.

### Remote Folder
Used to run the image on a remote server. Upload this folder to the remote server after configuration env/.override.env, .env, and docker-compose.yml

### Local Folder
Used to run the server locally for testing.

### Tools
1. Used to repair player data