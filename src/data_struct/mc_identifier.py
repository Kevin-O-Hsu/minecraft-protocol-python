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
from .mc_varint import McVarInt
import re


class McIdentifier(McDataStruct):
    
    def __init__(self, *,  bytes_content:bytes=bytes(), data_content:tuple[str, str]=tuple()) -> None:
        # data_content: (namespace, value)
        
        assert True in [bool(item) for item in (bytes_content, data_content)]\
            , "Either bytes_content or data_content must be provided"
        if bool(data_content):
            assert bool(re.fullmatch("[a-z0-9.-_]", data_content[0]))
            assert bool(re.fullmatch("[a-z0-9.-_/]"), data_content[1])
        
        self.bytes_content = bytes_content
        self.data_content = data_content
        
        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content == tuple():
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data:tuple[str, str]) -> bytes:
        """
        Encode the Identifier as a Minecraft VarInt-prefixed UTF-8 string.
        """
        # Format: namespace:value
        namespace = data[0]
        value = data[1]
        
        full_string = f"{namespace}:{value}"
        utf8_bytes = full_string.encode("utf-8")
        length_bytes = McVarInt(data_content=len(utf8_bytes)).bytes_content
        return length_bytes + utf8_bytes

    def data_decode(self, data: bytes) -> str:
        """
        Decode a Minecraft VarInt-prefixed UTF-8 string back into an Identifier (namespace:value).
        """
        length, length_size = McVarInt(bytes_content=data).decode_varint_with_size()
        str_bytes = data[length_size:length_size + length]
        decoded_string = str_bytes.decode('utf-8')
        return decoded_string, length_size + length