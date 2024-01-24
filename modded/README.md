### Mods/Plugins
1. Modify .env VANILLA_REPOSITORY to point to vanilla server file image
2. Modify .env MODDED_REPOSITORY to point to modded server file image that you will deploy
3. Modify Dockerfile to copy mods/plugins
4. pipenv run py push.py
5. You will be using this image instead of the vanilla one in your server docker-compose.yml if you want mods and plugins