
def encode_varint(value: int) -> bytes:
    """Encodes an integer to Minecraft VarInt format (max 5 bytes)."""
    result = bytearray()
    for _ in range(5):
        temp = value & 0x7F  # 取低7位
        value >>= 7
        if value != 0:
            result.append(temp | 0x80)  # 设置 continuation bit
        else:
            result.append(temp)
            return bytes(result)
    raise ValueError("VarInt is too big (more than 5 bytes)")


def encode_varlong(value: int) -> bytes:
    """Encodes an integer to Minecraft VarLong format (max 10 bytes)."""
    result = bytearray()
    for _ in range(10):
        temp = value & 0x7F  # 取低7位
        value >>= 7
        if value != 0:
            result.append(temp | 0x80)
        else:
            result.append(temp)
            return bytes(result)
    raise ValueError("VarLong is too big (more than 10 bytes)")

def decode_varint_with_size(data: bytes) -> tuple[int, int]:
    """
    Decode a Minecraft-style VarInt from bytes and return (value, bytes_used).
    """
    num_read = 0
    result = 0
    for i in range(min(5, len(data))):
        byte = data[i]
        result |= (byte & 0x7F) << (7 * i)
        num_read += 1
        if (byte & 0x80) == 0:
            return result, num_read
    raise ValueError("VarInt is too long or incomplete")

if __name__ == "__main__":
    print(encode_varint(1234567890))
    print(encode_varlong(1234567890123456789))