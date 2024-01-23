import subprocess
import zlib


UESAVE_TYPE_MAPS = [
    ".worldSaveData.CharacterSaveParameterMap.Key=Struct",
    ".worldSaveData.FoliageGridSaveDataMap.Key=Struct",
    ".worldSaveData.FoliageGridSaveDataMap.ModelMap.InstanceDataMap.Key=Struct",
    ".worldSaveData.MapObjectSpawnerInStageSaveData.Key=Struct",
    ".worldSaveData.ItemContainerSaveData.Key=Struct",
    ".worldSaveData.CharacterContainerSaveData.Key=Struct",
]


def uesave_params_forward(uesave_path, out_path):
    args = [
        uesave_path,
        'to-json',
        '--output', out_path,
    ]
    for map_type in UESAVE_TYPE_MAPS:
        args.append('--type')
        args.append(f'{map_type}')
    return args


def uesave_params_backward(uesave_path, input_file, output_file):
    args = [
        uesave_path,
        'from-json',
        '--input', input_file,
        '--output', output_file,
    ]
    return args


def json_to_sav(file, uesave_path="./lib/uesave"):
    gvas_file = file.replace('.sav.json', '.sav.gvas')
    sav_file = file.replace('.sav.json', '.sav')
    uesave_run = subprocess.run(uesave_params_backward(uesave_path, file, gvas_file))
    if uesave_run.returncode != 0:
        print(f'uesave.exe failed to convert {file} (return {uesave_run.returncode})')
        exit(1)
    # Open the old sav file to get type
    with open(sav_file, 'rb') as f:
        data = f.read()
        save_type = data[11]
    # Open the binary file
    with open(gvas_file, 'rb') as f:
        # Read the file
        data = f.read()
        uncompressed_len = len(data)
        compressed_data = zlib.compress(data)
        compressed_len = len(compressed_data)
        if save_type == 0x32:
            compressed_data = zlib.compress(compressed_data)
        with open(sav_file, 'wb') as f:
            f.write(uncompressed_len.to_bytes(4, byteorder='little'))
            f.write(compressed_len.to_bytes(4, byteorder='little'))
            f.write(b'PlZ')
            f.write(bytes([save_type]))
            f.write(bytes(compressed_data))
    print(f'Converted {file} to {sav_file}')


def sav_to_json(file, uesave_path="./lib/uesave"):
    with open(file, 'rb') as f:
        # Read the file
        data = f.read()
        uncompressed_len = int.from_bytes(data[0:4], byteorder='little')
        compressed_len = int.from_bytes(data[4:8], byteorder='little')
        magic_bytes = data[8:11]
        save_type = data[11]
        # Check for magic bytes
        if data[8:11] != b'PlZ':
            print(f'File {file} is not a save file, found {magic_bytes} instead of P1Z')
            exit(1)
        # Valid save types
        if save_type not in [0x30, 0x31, 0x32]:
            print(f'File {file} has an unknown save type: {save_type}')
            exit(1)
        # We only have 0x31 (single zlib) and 0x32 (double zlib) saves
        if save_type not in [0x31, 0x32]:
            print(f'File {file} uses an unhandled compression type: {save_type}')
            exit(1)
        if save_type == 0x31:
            # Check if the compressed length is correct
            if compressed_len != len(data) - 12:
                print(f'File {file} has an incorrect compressed length: {compressed_len}')
                exit(1)
        # Decompress file
        uncompressed_data = zlib.decompress(data[12:])
        if save_type == 0x32:
            # Check if the compressed length is correct
            if compressed_len != len(uncompressed_data):
                print(f'File {file} has an incorrect compressed length: {compressed_len}')
                exit(1)
            # Decompress file
            uncompressed_data = zlib.decompress(uncompressed_data)
        # Check if the uncompressed length is correct
        if uncompressed_len != len(uncompressed_data):
            print(f'File {file} has an incorrect uncompressed length: {uncompressed_len}')
            exit(1)
        # Save the uncompressed file
        with open(file + '.gvas', 'wb') as f:
            f.write(uncompressed_data)
        print(f'File {file} uncompressed successfully')
        # Convert to json with uesave
        # Run uesave.exe with the uncompressed file piped as stdin
        # Standard out will be the json string
        uesave_run = subprocess.run(uesave_params_forward(uesave_path, file+'.json'), input=uncompressed_data, capture_output=True)
        # Check if the command was successful
        if uesave_run.returncode != 0:
            print(f'uesave.exe failed to convert {file} (return {uesave_run.returncode})')
            print(uesave_run.stdout.decode('utf-8'))
            print(uesave_run.stderr.decode('utf-8'))
            exit(1)
        print(f'File {file} (type: {save_type}) converted to JSON successfully')
