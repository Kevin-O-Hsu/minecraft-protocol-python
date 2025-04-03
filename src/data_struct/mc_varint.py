# Minecraft-Protocol-Python
# Copyright (C) 2025  GreshAnt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from .datastruck import McDataStruct


class McVarInt(McDataStruct):
    def __init__(
        self, *, bytes_content: bytes = bytes(), data_content: int = None
    ) -> None:
        """
        VarInts are never longer than 5 bytes.
        Variable-length format such that smaller numbers use fewer bytes.
        These are very similar to Protocol Buffer Varints:
        the 7 least significant bits are used to encode the value and the most significant bit indicates whether there's another byte after it for the next part of the number.
        The least significant group is written first,
        followed by each of the more significant groups;
        thus, VarInts are effectively little endian (however, groups are 7 bits, not 8).
        """
        # Ensure that at least one of bytes_content or data_content is provided
        if data_content == 0:
            if bool(bytes_content):
                raise ValueError(
                    "You must provide exactly one of bytes_content or data_content."
                )
        elif bool(bytes_content) + bool(data_content) != 1:
            raise ValueError(
                "You must provide exactly one of bytes_content or data_content."
            )

        self.bytes_content = bytes_content
        self.data_content = data_content

        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content is None:
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data: int) -> bytes:
        """Encodes an integer to Minecraft VarInt format (max 5 bytes)."""

        # Minecraft VarInt 支持的范围是 int32 (即 -2147483648 到 2147483647)
        if data < -2147483648 or data > 2147483647:
            raise ValueError("VarInt is too big (more than 5 bytes)")

        if data < 0:
            data += 1 << 32  # Unsigned int32

        result = bytearray()
        for _ in range(5):
            temp = data & 0x7F  # 取最低7位
            data >>= 7  # 右移7位

            if data != 0:  # 如果还有更多数据
                result.append(temp | 0x80)  # 设置继续位为1
            else:
                result.append(temp)
                return bytes(result)

    def data_decode(self, data: bytes) -> int:
        """Decodes a Minecraft VarInt from bytes."""
        result = 0
        shift = 0
        for i, byte in enumerate(data):
            result |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:  # continuation bit = 0, we're done
                break
            shift += 7
        else:
            raise ValueError("VarInt is too big (more than 5 bytes)")

        # ✔ 添加符号扩展判断（Minecraft 的 VarInt 是 int32）
        if result >= 1 << 31:
            result -= 1 << 32

        return result

    def decode_varint_with_size(self) -> tuple[int, int]:
        """
        Decode a Minecraft-style VarInt from bytes and return (value, bytes_used).
        """
        num_read = 0
        result = 0
        for i in range(min(5, len(self.bytes_content))):
            byte = self.bytes_content[i]
            result |= (byte & 0x7F) << (7 * i)
            num_read += 1
            if (byte & 0x80) == 0:
                return result, num_read
        raise ValueError("VarInt is too long or incomplete")
