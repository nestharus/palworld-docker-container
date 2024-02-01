#!/bin/bash

echo "Initializing Engine Configuratio"

CONFIG_FILEPATH="/palworld/Pal/Saved/Config/LinuxServer"
ENGINE_SETTINGS_FILEPATH="${CONFIG_FILEPATH}/Engine.ini"

if [ -f "${ENGINE_SETTINGS_FILEPATH}" ]; then
    echo "Engine Configuration Found"
    chmod u+rw "${ENGINE_SETTINGS_FILEPATH}"
    rm ${ENGINE_SETTINGS_FILEPATH}
fi

cat > "${ENGINE_SETTINGS_FILEPATH}" << EOF
[Core.System]
Paths=../../../Engine/Content
Paths=%GAMEDIR%Content
Paths=../../../Engine/Plugins/2D/Paper2D/Content
Paths=../../../Engine/Plugins/Animation/ControlRigSpline/Content
Paths=../../../Engine/Plugins/Animation/ControlRig/Content
Paths=../../../Engine/Plugins/Animation/IKRig/Content
Paths=../../../Engine/Plugins/Animation/MotionWarping/Content
Paths=../../../Engine/Plugins/Bridge/Content
Paths=../../../Engine/Plugins/Compositing/Composure/Content
Paths=../../../Engine/Plugins/Compositing/OpenColorIO/Content
Paths=../../../Engine/Plugins/Developer/AnimationSharing/Content
Paths=../../../Engine/Plugins/Developer/Concert/ConcertSync/ConcertSyncClient/Content
Paths=../../../Engine/Plugins/Editor/BlueprintHeaderView/Content
Paths=../../../Engine/Plugins/Editor/GeometryMode/Content
Paths=../../../Engine/Plugins/Editor/ModelingToolsEditorMode/Content
Paths=../../../Engine/Plugins/Editor/ObjectMixer/LightMixer/Content
Paths=../../../Engine/Plugins/Editor/ObjectMixer/ObjectMixer/Content
Paths=../../../Engine/Plugins/Editor/SpeedTreeImporter/Content
Paths=../../../Engine/Plugins/Enterprise/DatasmithContent/Content
Paths=../../../Engine/Plugins/Enterprise/GLTFExporter/Content
Paths=../../../Engine/Plugins/Experimental/ChaosCaching/Content
Paths=../../../Engine/Plugins/Experimental/ChaosClothEditor/Content
Paths=../../../Engine/Plugins/Experimental/ChaosNiagara/Content
Paths=../../../Engine/Plugins/Experimental/ChaosSolverPlugin/Content
Paths=../../../Engine/Plugins/Experimental/CommonUI/Content
Paths=../../../Engine/Plugins/Experimental/Dataflow/Content
Paths=../../../Engine/Plugins/Experimental/FullBodyIK/Content
Paths=../../../Engine/Plugins/Experimental/GeometryCollectionPlugin/Content
Paths=../../../Engine/Plugins/Experimental/GeometryFlow/Content
Paths=../../../Engine/Plugins/Experimental/ImpostorBaker/Content
Paths=../../../Engine/Plugins/Experimental/Landmass/Content
Paths=../../../Engine/Plugins/Experimental/MeshLODToolset/Content
Paths=../../../Engine/Plugins/Experimental/PythonScriptPlugin/Content
Paths=../../../Engine/Plugins/Experimental/StaticMeshEditorModeling/Content
Paths=../../../Engine/Plugins/Experimental/UVEditor/Content
Paths=../../../Engine/Plugins/Experimental/Volumetrics/Content
Paths=../../../Engine/Plugins/Experimental/Water/Content
Paths=../../../Engine/Plugins/FX/Niagara/Content
Paths=../../../Engine/Plugins/JsonBlueprintUtilities/Content
Paths=../../../Engine/Plugins/Media/MediaCompositing/Content
Paths=../../../Engine/Plugins/Media/MediaPlate/Content
Paths=../../../Engine/Plugins/MovieScene/MovieRenderPipeline/Content
Paths=../../../Engine/Plugins/MovieScene/SequencerScripting/Content
Paths=../../../Engine/Plugins/NiagaraUIRenderer/Content
Paths=../../../Engine/Plugins/PivotTool/Content
Paths=../../../Engine/Plugins/PlacementTools/Content
Paths=../../../Engine/Plugins/Runtime/AudioSynesthesia/Content
Paths=../../../Engine/Plugins/Runtime/AudioWidgets/Content
Paths=../../../Engine/Plugins/Runtime/GeometryProcessing/Content
Paths=../../../Engine/Plugins/Runtime/Metasound/Content
Paths=../../../Engine/Plugins/Runtime/ResonanceAudio/Content
Paths=../../../Engine/Plugins/Runtime/SunPosition/Content
Paths=../../../Engine/Plugins/Runtime/Synthesis/Content
Paths=../../../Engine/Plugins/Runtime/WaveTable/Content
Paths=../../../Engine/Plugins/Runtime/WebBrowserWidget/Content
Paths=../../../Engine/Plugins/SkyCreatorPlugin/Content
Paths=../../../Engine/Plugins/VirtualProduction/CameraCalibrationCore/Content
Paths=../../../Engine/Plugins/VirtualProduction/LiveLinkCamera/Content
Paths=../../../Engine/Plugins/VirtualProduction/Takes/Content
Paths=../../../Engine/Plugins/Web/HttpBlueprint/Content
Paths=../../../Pal/Plugins/DLSS/Content
Paths=../../../Pal/Plugins/EffectsChecker/Content
Paths=../../../Pal/Plugins/FSR2MovieRenderPipeline/Content
Paths=../../../Pal/Plugins/FSR2/Content
Paths=../../../Pal/Plugins/HoudiniEngine/Content
Paths=../../../Pal/Plugins/PPSkyCreatorPlugin/Content
Paths=../../../Pal/Plugins/PocketpairUser/Content
Paths=../../../Pal/Plugins/SpreadSheetToCsv/Content
Paths=../../../Pal/Plugins/Wwise/Content

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

[/script/onlinesubsystemutils.ipnetdriver]
NetServerMaxTickRate=120
NetClientTicksPerSecond=120   ; Increases the update frequency for clients, enhancing responsiveness and reducing lag.
EOF

chown steam:steam "${ENGINE_SETTINGS_FILEPATH}"
chmod u-wx "${ENGINE_SETTINGS_FILEPATH}"

echo "Wrote Engine Configuration"

cat "${ENGINE_SETTINGS_FILEPATH}"