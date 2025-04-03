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


from .mc_string import McString
from .datastruck import McDataStruct

class McArray(McDataStruct):
    
    def __init__(self, *,  bytes_content:bytes=bytes(), data_content:list=list(), count:int=None) -> None:
        """
        Represents a list where the length is not encoded. 
        The length must be known from the context. 
        If the array is empty nothing will be encoded.
        """
        assert True in [bool(item) for item in (bytes_content, data_content)]\
            , "Either bytes_content or data_content must be provided"
        
        
        self.bytes_content = bytes_content
        self.data_content = data_content
        self.count = count
        
        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif ((self.data_content == list()) and (self.count is not None)):
            self.data_content = self.data_decode(self.bytes_content, self.count)
    
    def data_encode(self, data:list) -> bytes:
        """
        Encode a list of strings as a Minecraft-style string array.
        Each string is encoded as [VarInt(length) + UTF-8 bytes].
        No array length is included — must be known by context.
        """
        return b''.join(McString(data_content=s).bytes_content for s in data)
    
    def data_decode(self, data: bytes, count:int) -> list[str]:
        """
        Decode a Minecraft-style string array from bytes, given the known string count.
        Returns a list of strings.
        """
        strings = []
        offset = 0
        for _ in range(count):
            s, size = McString(bytes_content=data[offset:]).data_content
            strings.append(s)
            offset += size
        return strings
