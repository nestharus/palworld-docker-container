#!/bin/bash

echo "Initializing Engine Configuratio"

ENGINE_SETTINGS_FOLDER="/palworld/Pal/Plugins/Wwise/Content"
ENGINE_SETTINGS_FILEPATH="${ENGINE_SETTINGS_FOLDER}/Engine.ini"

if [ ! -d "${ENGINE_SETTINGS_FOLDER}" ]; then
    mkdir -p "${ENGINE_SETTINGS_FOLDER}"
    chown -R steam:steam ${ENGINE_SETTINGS_FOLDER}
fi

if [ -f "${ENGINE_SETTINGS_FILEPATH}" ]; then
    echo "Engine Configuration Found"
    chmod u+rw "${ENGINE_SETTINGS_FILEPATH}"
    rm ${ENGINE_SETTINGS_FILEPATH}
fi

cat > "${ENGINE_SETTINGS_FILEPATH}" << EOF
; Online Subsystem Utils Configuration
; Adjusting tick rates for LAN and Internet servers to enhance the frequency of game state updates,
; leading to smoother gameplay and less desynchronization between server and clients.
[/script/onlinesubsystemutils.ipnetdriver]
LanServerMaxTickRate=120  ; Sets maximum ticks per second for LAN servers, higher rates result in smoother gameplay.
NetServerMaxTickRate=120  ; Sets maximum ticks per second for Internet servers, similarly ensuring smoother online gameplay.

; Player Configuration
; These settings are crucial for optimizing the network bandwidth allocation per player,
; allowing for more data to be sent and received without bottlenecking.
[/script/engine.player]
ConfiguredInternetSpeed=104857600  ; Sets the assumed player internet speed in bytes per second. High value reduces chances of bandwidth throttling.
ConfiguredLanSpeed=104857600       ; Sets the LAN speed, ensuring LAN players can utilize maximum network capacity.

; Socket Subsystem Epic Configuration
; Tailoring the max client rate for both local and internet clients, this optimizes data transfer rates,
; ensuring that the server can handle high volumes of data without causing lag.
[/script/socketsubsystemepic.epicnetdriver]
MaxClientRate=104857600          ; Maximum data transfer rate per client for all connections, set to a high value to prevent data capping.
MaxInternetClientRate=104857600  ; Specifically targets internet clients, allowing for high-volume data transfer without restrictions.

; Engine Configuration
; These settings manage how the game's frame rate is handled, which can impact how smoothly the game runs.
; Smoother frame rates can lead to a better synchronization between client and server.
[/script/engine.engine]
bSmoothFrameRate=true    ; Enables the game engine to smooth out frame rate fluctuations for a more consistent visual experience.
bUseFixedFrameRate=false ; Disables the use of a fixed frame rate, allowing the game to dynamically adjust frame rate for optimal performance.
SmoothedFrameRateRange=(LowerBound=(Type=Inclusive,Value=30.000000),UpperBound=(Type=Exclusive,Value=120.000000)) ; Sets a target frame rate range for smoothing.
MinDesiredFrameRate=60.000000 ; Specifies a minimum acceptable frame rate, ensuring the game runs smoothly at least at this frame rate.
FixedFrameRate=120.000000     ; (Not active due to bUseFixedFrameRate set to false) Placeholder for a fixed frame rate if needed.
NetClientTicksPerSecond=120   ; Increases the update frequency for clients, enhancing responsiveness and reducing lag.
EOF

chown steam:steam "${ENGINE_SETTINGS_FILEPATH}"
chmod u-wx "${ENGINE_SETTINGS_FILEPATH}"

echo "Wrote Engine Configuration"

cat "${ENGINE_SETTINGS_FILEPATH}"