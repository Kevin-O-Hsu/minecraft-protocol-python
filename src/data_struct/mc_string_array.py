from .mc_string import decode_string, encode_string

def encode_string_array(strings: list[str]) -> bytes:
    """
    Encode a list of strings as a Minecraft-style string array.
    Each string is encoded as [VarInt(length) + UTF-8 bytes].
    No array length is included — must be known by context.
    """
    return b''.join(encode_string(s) for s in strings)

def decode_string_array(data: bytes, count: int) -> list[str]:
    """
    Decode a Minecraft-style string array from bytes, given the known string count.
    Returns a list of strings.
    """
    strings = []
    offset = 0
    for _ in range(count):
        s, size = decode_string(data[offset:])
        strings.append(s)
        offset += size
    return strings

