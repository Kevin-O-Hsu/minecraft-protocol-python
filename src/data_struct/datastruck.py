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


from abc import ABC, abstractmethod

class McDataStruct(ABC):
    
    def __init__(self, *,  bytes_content:bytes=bytes(), data_content:tuple=tuple()) -> None:
        
        assert True in [bool(item) for item in (bytes_content, data_content)]\
            , "Either bytes_content or data_content must be provided"
        
        
        self.bytes_content = bytes_content
        self.data_content = data_content
        
        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content == tuple():
            self.data_content = self.data_decode(self.bytes_content)

    @abstractmethod
    def data_decode(self, bytes_content:bytes) -> tuple:
        """
        Override this method to convert bytes_content to data_content
        """
        pass

    @abstractmethod
    def data_encode(self, data_content:tuple) -> bytes:
        """
        Override this method to convert data_content to bytes_content
        """
        pass
