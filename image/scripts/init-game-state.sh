#!/bin/bash

echo "Initializing Game State"

GAME_USER_SETTINGS_FILEPATH="/palworld/Pal/Saved/Config/LinuxServer/GameUserSettings.ini"

if [ -f "${GAME_USER_SETTINGS_FILEPATH}" ]; then
    echo "Game State Configuration Found"
    chmod u+rw "${GAME_USER_SETTINGS_FILEPATH}"
    rm ${GAME_USER_SETTINGS_FILEPATH}
fi

if [ ! -d "/palworld/Pal/Saved/SaveGames" ]; then
    echo "No Game State Profile Present"
    exit 1
fi

chown -R steam:steam /palworld/Pal/Saved/SaveGames

if [ ! "$(ls -A /palworld/Pal/Saved/SaveGames)" ]; then
    echo "No Game State Profile Present"
    exit 1
fi

if [ ! "$(ls -A /palworld/Pal/Saved/SaveGames/0)" ]; then
    echo "No Game State Profile Present"
    exit 1
fi

echo "Mounted Game State Volume"

ls -laR "/palworld/Pal/Saved/SaveGames"

GAME_STATE_PROFILE=$(find "/palworld/Pal/Saved/SaveGames/0" -maxdepth 1 -type d -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")
GAME_STATE_PROFILE=$(basename "${GAME_STATE_PROFILE}")

echo "Game State Profile Found"

echo "${GAME_STATE_PROFILE}"

cat > "${GAME_USER_SETTINGS_FILEPATH}" << EOF
[/Script/Pal.PalGameLocalSettings]
AudioSettings=(Master=0.500000,BGM=1.000000,SE=1.000000,PalVoice=1.000000,HumanVoice=1.000000,Ambient=1.000000,UI=1.000000)
GraphicsLevel=None
DefaultGraphicsLevel=None
bRunedBenchMark=False
bHasAppliedUserSetting=False
DedicatedServerName=${GAME_STATE_PROFILE}
AntiAliasingType=AAM_TSR
DLSSMode=Performance
GraphicsCommonQuality=0
EOF

chown steam:steam "${GAME_USER_SETTINGS_FILEPATH}"
chmod u-wx "${GAME_USER_SETTINGS_FILEPATH}"

echo "Wrote Game State Configuration With Profile"

cat "${GAME_USER_SETTINGS_FILEPATH}"