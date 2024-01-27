import json
import subprocess


UESAVE_TYPE_MAPS = [
    ".worldSaveData.CharacterSaveParameterMap.Key=Struct",
    ".worldSaveData.FoliageGridSaveDataMap.Key=Struct",
    ".worldSaveData.FoliageGridSaveDataMap.ModelMap.InstanceDataMap.Key=Struct",
    ".worldSaveData.MapObjectSpawnerInStageSaveData.Key=Struct",
    ".worldSaveData.ItemContainerSaveData.Key=Struct",
    ".worldSaveData.CharacterContainerSaveData.Key=Struct",
]


def uesave_params_forward(uesave_path):
    args = [
        uesave_path,
        'to-json'
    ]
    for map_type in UESAVE_TYPE_MAPS:
        args.append('--type')
        args.append(f'{map_type}')
    return args


def uesave_params_backward(uesave_path):
    args = [
        uesave_path,
        'from-json'
    ]
    return args


def json_to_gvas(json_data, uesave_path="./lib/sav/uesave"):
    json_str = json.dumps(json_data)
    json_bytes = json_str.encode()

    uesave_run = subprocess.run(uesave_params_backward(uesave_path), input=json_bytes, capture_output=True)

    if uesave_run.returncode != 0:
        print(f'uesave.exe failed to convert to gvas (return {uesave_run.returncode})')
        return None

    return uesave_run.stdout


def gvas_to_json(gvas: bytes, uesave_path="./lib/sav/uesave"):
    uesave_run = subprocess.run(uesave_params_forward(uesave_path), input=gvas, capture_output=True)

    # Check if the command was successful
    if uesave_run.returncode != 0:
        print(f'uesave.exe failed to convert (return {uesave_run.returncode})')
        print(uesave_run.stdout.decode('utf-8'))
        print(uesave_run.stderr.decode('utf-8'))
        return None

    json_data = uesave_run.stdout
    json_data = json_data.decode()
    json_data = json.loads(json_data)

    return json_data
