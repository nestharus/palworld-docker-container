import json
import re
import string
import struct
from io import BytesIO

from lib.uesave import *


def get_world_guids(level_sav_json):
    world_guids = {}

    for record in level_sav_json['root']['properties']['worldSaveData']['Struct']['value']['Struct']['CharacterSaveParameterMap']['Map']['value']:
        if record['key']['Struct']['Struct']['PlayerUId']['Struct']['value']['Guid'] != "00000000-0000-0000-0000-000000000000":
            guid = record['key']['Struct']['Struct']['PlayerUId']['Struct']['value']['Guid']
            guid = guid.upper()
            world_guids[guid] = record

    return world_guids


def get_world_record_guid(record):
    return record['key']['Struct']['Struct']['PlayerUId']['Struct']['value']['Guid'].upper()


def get_world_records(level_sav_json):
    return level_sav_json['root']['properties']['worldSaveData']['Struct']['value']['Struct']['CharacterSaveParameterMap']['Map']['value']


def set_world_records(level_sav_json, records):
    level_sav_json['root']['properties']['worldSaveData']['Struct']['value']['Struct']['CharacterSaveParameterMap']['Map']['value'] = records


def patch_world_guid(level_sav_json, world_guids):
    records = [
        world_guids[get_world_record_guid(record)]
        if get_world_record_guid(record) in world_guids
        else record
        for record in get_world_records(level_sav_json)
    ]

    set_world_records(level_sav_json, records)


def load_world_json(directory, game_profile):
    with open(f'{directory}/0/{game_profile}/Level.sav.json', 'r') as f:
        data = json.load(f)

    return data


def load_player_json(directory, game_profile, player_guid):
    with open(f'{directory}/0/{game_profile}/Players/{player_guid.replace("-", "")}.sav.json', 'r') as f:
        data = json.load(f)

    return data


def save_world_json(directory, game_profile, data):
    with open(f'{directory}/0/{game_profile}/Level.sav.json', 'w') as f:
        json.dump(data, f)


def save_player_json(directory, game_profile, player_guid, data):
    with open(f'{directory}/0/{game_profile}/Players/{player_guid.replace("-", "")}.sav.json', 'w') as f:
        json.dump(data, f)


def world_to_json(directory, game_profile):
    sav_to_json(f'{directory}/0/{game_profile}/Level.sav')


def world_to_sav(directory, game_profile):
    json_to_sav(f'{directory}/0/{game_profile}/Level.sav.json')


def player_to_json(directory, game_profile, player_guid):
    sav_to_json(f'{directory}/0/{game_profile}/Players/{player_guid.replace("-", "")}.sav')


def player_to_sav(directory, game_profile, player_guid):
    json_to_sav(f'{directory}/0/{game_profile}/Players/{player_guid.replace("-", "")}.sav.json')


def is_player_blank(player_data):
    save_data = player_data["root"]["properties"]["SaveData"]["Struct"]["value"]["Struct"]
    recipes = save_data["UnlockedRecipeTechnologyNames"]["Array"]["value"]["Base"]["Name"]
    # has_technology_points = "TechnologyPoint" in save_data
    # has_records = "RecordData" in save_data

    return len(recipes) == 5  # and not has_technology_points and not has_records


def get_world_group_records(level_save_json):
    return level_save_json['root']['properties']['worldSaveData']['Struct']['value']['Struct']['GroupSaveDataMap']['Map']['value']


def get_guilds(level_save_json):
    return [
        get_guild_data(record)
        for record in get_world_group_records(level_save_json)
        if 'Guild' in get_world_group_record_type(record)
    ]


def get_world_group_record_type(record):
    return record['value']['Struct']['Struct']['GroupType']['Enum']['value']


def get_guild_data(record):
    return bytes(record['value']['Struct']['Struct']['RawData']['Array']['value']["Base"]["Byte"]["Byte"])


def read_str(stream):
    length = struct.unpack('i', stream.read(4))[0]
    if length > 0:
        return stream.read(length)
    else:
        length = - length * 2
        return stream.read(length).decode('utf-16')


def differentiate_bytes_and_strings(data):
    result = ''
    for byte in data:
        char = chr(byte)
        if char in string.printable:
            result += char
    return result


def get_guild_user_guids(guild_bytes: bytes):
    guids = []

    stream = BytesIO(guild_bytes)
    _unknown = stream.read(16)

    group_id = read_str(stream)
    # group guid
    # print(group_id)
    struct.unpack('I', stream.read(4))[0]

    # guildless
    if b'Unnamed Guild' in guild_bytes:
        stream.seek(guild_bytes.index(b'Unnamed Guild') - 4)
    elif b'Astrals Simps' in guild_bytes:
        stream.seek(guild_bytes.index(b'Astrals Simps') - 4)
    else:
        strings = re.findall(r'[ -~]+', differentiate_bytes_and_strings(guild_bytes))
        print(strings)
        return guids

    group_name = read_str(stream)
    print(group_name)

    hex_id = stream.read(16)
    # print(hex_id.hex())

    member_count = struct.unpack('I', stream.read(4))[0]
    print(member_count)

    for _ in range(member_count):
        # print('='*50)
        hex_id = stream.read(16)
        hex_id = b''.join([hex_id[i:i+4][::-1] for i in range(0,len(hex_id),4)]) # fix byteorder
        # guid
        print(hex_id.hex())
        guids.append(hex_id.hex()[2:34])
        stream.read(4).hex()
        stream.read(4).hex()
        # name
        print(read_str(stream))

    return guids
