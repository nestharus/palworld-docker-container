FROM cm2network/steamcmd:root as build_stage
LABEL authors="nestharus"

ENV STEAMAPPID 2394010

RUN apt-get update && \
	apt-get -y install --no-install-recommends lib32gcc-s1 lib32stdc++6 lib32z1 && \
	rm -rf /var/lib/apt/lists/*

VOLUME ["/app"]

ENTRYPOINT bash ./steamcmd.sh +force_install_dir /app +login anonymous +app_update ${STEAMAPPID} validate +quit && \
           mkdir -p /app/Pal/Saved && \
           chmod a+w /app/Pal/Saved && \
           chown -R steam:steam /app && \
           chmod +x "/app/PalServer.sh" && \
           su steam -c "/app/PalServer.sh -port 8211 -players 4"