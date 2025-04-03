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


class McPosition(McDataStruct):

    def __init__(
        self,
        *,
        bytes_content: bytes = bytes(),
        data_content: tuple[int, int, int] = tuple()
    ) -> None:

        assert True in [
            bool(item) for item in (bytes_content, data_content)
        ], "Either bytes_content or data_content must be provided"

        self.bytes_content = bytes_content
        self.data_content = data_content

        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content == tuple():
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data: tuple[int, int, int]) -> bytes:
        """
        Encode (x, y, z) block position into 8-byte big-endian Position field (Minecraft format).
        - x: 26-bit signed int
        - z: 26-bit signed int
        - y: 12-bit signed int
        """
        # 将负数处理成补码形式（保留下位）
        x, y, z = data
        x &= 0x3FFFFFF  # 26位
        y &= 0xFFF  # 12位
        z &= 0x3FFFFFF  # 26位
        packed = (x << 38) | (z << 12) | y
        return packed.to_bytes(8, byteorder="big", signed=True)

    def data_decode(self, data: bytes) -> tuple[int, int, int]:
        """
        Decode 8-byte Position field into (x, y, z) block position.
        - x: 26-bit signed int
        - y: 12-bit signed int
        - z: 26-bit signed int
        """
        # 从字节数据中解码出 64 位整数（有符号）
        packed = int.from_bytes(data, byteorder="big", signed=True)

        # 提取 x, y, z
        x = (packed >> 38) & 0x3FFFFFF  # 26-bit
        y = (packed >> 26) & 0xFFF  # 12-bit
        z = packed & 0x3FFFFFF  # 26-bit

        return (x, y, z)
