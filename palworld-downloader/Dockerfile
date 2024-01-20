FROM cm2network/steamcmd:root as download_stage
LABEL authors="nestharus"

ENV STEAMAPPID 2394010

USER steam

ENTRYPOINT bash ./steamcmd.sh +force_install_dir /downloaded +login anonymous +app_update ${STEAMAPPID} validate +quit