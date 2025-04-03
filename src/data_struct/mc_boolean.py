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


class McBoolean(McDataStruct):

    def __init__(
        self, *, bytes_content: bytes = bytes(), data_content: bool = None
    ) -> None:
        assert (
            bytes_content or data_content is not None
        ), "Either bytes_content or data_content must be provided."
        assert isinstance(data_content, bool), "data_content must be a boolean."

        self.bytes_content = bytes_content
        self.data_content = data_content

        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content is None:
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data: bool) -> bytes:
        """
        Encode a boolean value into 1 byte:
        True -> 0x01, False -> 0x00
        """
        return b"\x01" if data else b"\x00"

    def data_decode(self, data: bytes) -> bool:
        """
        Decode a 1-byte boolean from bytes.
        """
        if len(data) != 1:
            raise ValueError("Boolean must be exactly 1 byte")
        return data[0] != 0
