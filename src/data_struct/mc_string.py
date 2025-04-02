
def encode_string(s: str) -> bytes:
    """
    Encode a string as Minecraft VarInt-prefixed UTF-8 string.
    """
    utf8_bytes = s.encode('utf-8')
    length_bytes = encode_varint(len(utf8_bytes))
    return length_bytes + utf8_bytes

def decode_string(data: bytes) -> tuple[str, int]:
    """
    Decode a Minecraft VarInt-prefixed UTF-8 string.
    Returns (string, total_bytes_consumed)
    """
    # 解码 VarInt 长度前缀
    length, length_size = decode_varint_with_size(data)
    str_bytes = data[length_size:length_size + length]
    s = str_bytes.decode('utf-8')
    return s, length_size + length
