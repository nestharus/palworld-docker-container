import struct
from io import BytesIO


def get_world_guids(level_sav_json):
    world_guids = {}

    for record in get_world_records(level_sav_json):
        if get_world_record_guid(record) != "00000000-0000-0000-0000-000000000000":
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


def get_player_guid(guild_bytes: bytes, guild_name, player_name):
    guids = []

    guild_name = guild_name.encode()

    if guild_name not in guild_bytes:
        return guids

    stream = BytesIO(guild_bytes)
    _unknown = stream.read(16)

    group_id = read_str(stream)
    # group guid
    # print(group_id)
    struct.unpack('I', stream.read(4))[0]

    stream.seek(guild_bytes.index(guild_name) - 4)

    group_name = read_str(stream).decode('utf-8')
    group_name = group_name.replace('\x00', '')

    hex_id = stream.read(16)
    # print(hex_id.hex())

    member_count = struct.unpack('I', stream.read(4))[0]

    print(f'{repr(group_name)}: ({member_count})')
    print('='*50)

    for _ in range(member_count):
        hex_id = stream.read(16)
        hex_id = b''.join([hex_id[i:i+4][::-1] for i in range(0,len(hex_id),4)]) # fix byteorder
        guid = hex_id.hex()
        guid = guid.upper()
        guid = guid[:8] + '-' + guid[8:12] + '-' + guid[12:16] + '-' + guid[16:20] + '-' + guid[20:]
        stream.read(4).hex()
        stream.read(4).hex()
        name = read_str(stream).decode('utf-8')
        name = name.replace('\x00', '')
        print(f'\t{repr(name)}: {repr(guid)}')

        if name == player_name:
            guids.append(guid)

    return guids
