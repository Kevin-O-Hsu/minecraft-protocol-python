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


from .mc_varint import McVarInt


class McString:

    def __init__(
        self, *, bytes_content: bytes = bytes(), data_content: str = str()
    ) -> None:
        """
        UTF-8 string prefixed with its size in bytes as a VarInt.
        Maximum length of n characters,
        which varies by context.
        The encoding used on the wire is regular UTF-8,
        not Java's "slight modification".
        However, the length of the string for purposes of the length limit is its number of UTF-16 code units,
        that is, scalar values > U+FFFF are counted as two.
        Up to n * 3 bytes can be used to encode a UTF-8 string comprising n code units when converted to UTF-16,
        and both of those limits are checked.
        Maximum n value is 32767.
        The + 3 is due to the max size of a valid length VarInt.
        """
        assert True in [
            bool(item) for item in (bytes_content, data_content)
        ], "Either bytes_content or data_content must be provided"

        self.bytes_content = bytes_content
        self.data_content = data_content

        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content == str():
            self.data_content = self.data_decode(self.bytes_content)[0]

    def data_encode(self, data: str) -> bytes:
        """
        Encode a string as Minecraft VarInt-prefixed UTF-8 string.
        """
        utf8_bytes = data.encode("utf-8")
        length_bytes = McVarInt(data_content=len(utf8_bytes)).bytes_content
        return length_bytes + utf8_bytes

    def data_decode(self, data: bytes) -> tuple[str, int]:
        """
        Decode a Minecraft VarInt-prefixed UTF-8 string.
        Returns (string, total_bytes_consumed)
        """
        # 解码 VarInt 长度前缀
        # length -> value
        length, length_size = McVarInt(bytes_content=data).decode_varint_with_size()
        str_bytes = data[length_size : length_size + length]
        s = str_bytes.decode("utf-8")
        return s, length_size + length
