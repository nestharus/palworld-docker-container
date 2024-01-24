import zlib
from typing import Union


def decompress_gvas(data: bytes) -> Union[None, tuple[bytes, int]]:
    uncompressed_len = int.from_bytes(data[0:4], byteorder='little')
    compressed_len = int.from_bytes(data[4:8], byteorder='little')
    magic_bytes = data[8:11]
    save_type = data[11]
    # Check for magic bytes
    if data[8:11] != b'PlZ':
        print(f'not a save, found {magic_bytes} instead of P1Z')
        return None
    # Valid save types
    if save_type not in [0x30, 0x31, 0x32]:
        print(f'unknown save type: {save_type}')
        return None
    # We only have 0x31 (single zlib) and 0x32 (double zlib) saves
    if save_type not in [0x31, 0x32]:
        print(f'unhandled compression type: {save_type}')
        return None
    if save_type == 0x31:
        # Check if the compressed length is correct
        if compressed_len != len(data) - 12:
            print(f'incorrect compressed length: {compressed_len}')
            return None
    # Decompress file
    uncompressed_data = zlib.decompress(data[12:])
    if save_type == 0x32:
        # Check if the compressed length is correct
        if compressed_len != len(uncompressed_data):
            print(f'incorrect compressed length: {compressed_len}')
            return None
        # Decompress file
        uncompressed_data = zlib.decompress(uncompressed_data)
    # Check if the uncompressed length is correct
    if uncompressed_len != len(uncompressed_data):
        print(f'incorrect uncompressed length: {uncompressed_len}')
        return None

    return uncompressed_data, save_type


def compress_gvas(data: bytes, save_type: int) -> bytes:
    uncompressed_len = len(data)
    compressed_data = zlib.compress(data)
    compressed_len = len(compressed_data)
    if save_type == 0x32:
        compressed_data = zlib.compress(compressed_data)

    # Create a byte array and append the necessary information
    result = bytearray()
    result.extend(uncompressed_len.to_bytes(4, byteorder='little'))
    result.extend(compressed_len.to_bytes(4, byteorder='little'))
    result.extend(b'PlZ')
    result.extend(bytes([save_type]))
    result.extend(compressed_data)

    return bytes(result)
