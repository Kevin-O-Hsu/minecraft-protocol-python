def encode_position_bytes(x: int, y: int, z: int) -> bytes:
    """
    Encode (x, y, z) block position into 8-byte big-endian Position field (Minecraft format).
    - x: 26-bit signed int
    - z: 26-bit signed int
    - y: 12-bit signed int
    """
    # 将负数处理成补码形式（保留下位）
    x &= 0x3FFFFFF  # 26位
    y &= 0xFFF      # 12位
    z &= 0x3FFFFFF  # 26位
    packed = (x << 38) | (z << 12) | y
    return packed.to_bytes(8, byteorder='big', signed=False)
