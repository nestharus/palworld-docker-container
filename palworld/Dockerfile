FROM debian:bookworm-slim
LABEL authors="nestharus"

ENV PALWORLD_PLAYERS 32

RUN apt-get update && \
	apt-get -y install --no-install-recommends lib32gcc-s1 lib32stdc++6 lib32z1 && \
	rm -rf /var/lib/apt/lists/*

VOLUME ["/app/Pal/Saved"]

RUN useradd -ms /bin/bash serveruser

COPY /target/app /app

RUN chmod a+w /app/Pal/Saved
RUN chmod +x "/app/PalServer.sh"
RUN chown -R serveruser:serveruser /app

EXPOSE 8211/udp
EXPOSE 25575/tcp

ENTRYPOINT su - serveruser -c "/app/PalServer.sh -port 8211 -players ${PALWORLD_PLAYERS} -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS"