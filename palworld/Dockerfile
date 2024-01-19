FROM cm2network/steamcmd:root
LABEL authors="nestharus"

VOLUME ["/app/Pal/Saved/SaveGames"]
VOLUME ["/app/Pal/Saved/Config"]

COPY /target/app /app

RUN chmod +x "/app/PalServer.sh"
RUN chown -R steam:steam /app
#RUN chmod -R 444 /app/Pal/Saved/Config/LinuxServer

RUN apt-get update && \
	apt-get -y install --no-install-recommends lib32gcc-s1 lib32stdc++6 lib32z1 && \
	rm -rf /var/lib/apt/lists/*

RUN mkdir ~/.steam
RUN ln -s /app/linux64 /home/steam/.steam/sdk64
RUN chown -R steam:steam /home/steam

COPY /start.sh ./start.sh
RUN chmod +x "./start.sh"

ENV PALWORLD_PLAYERS 32
ENV COMMUNITY false
ENV SERVER_PASSWORD password
ENV SERVER_NAME name
ENV PUBLIC_IP=1.1.1.1
ENV PUBLIC_PORT=8211
ENV MULTITHREADING=true

EXPOSE 8211/udp
EXPOSE 25575/tcp

ENTRYPOINT ./start.sh