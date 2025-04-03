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


class McShort(McDataStruct):

    def __init__(
        self, *, bytes_content: bytes = bytes(), data_content: int = None
    ) -> None:
        assert (
            bytes_content or data_content is not None
        ), "Either bytes_content or data_content must be provided."
        assert (
            -32768 <= data_content <= 32767
        ), "Value out of range for 16-bit signed integer"

        self.bytes_content = bytes_content
        self.data_content = data_content

        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content is None:
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data: int) -> bytes:
        """
        Encode a signed 16-bit integer into 2-byte big-endian bytes.
        Range: -32768 to 32767
        """
        if not (-32768 <= data <= 32767):
            raise ValueError("Value out of range for 16-bit signed integer")
        return data.to_bytes(2, byteorder="big", signed=True)

    def data_decode(self, data: bytes) -> int:
        """
        Decode 2-byte big-endian bytes into a signed 16-bit integer.
        """
        if len(data) != 2:
            raise ValueError("Expected exactly 2 bytes for a short")
        return int.from_bytes(data, byteorder="big", signed=True)
