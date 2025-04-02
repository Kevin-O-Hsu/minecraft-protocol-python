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

class McFixedPoints(McDataStruct):
    
    def __init__(self, *,  bytes_content:bytes=bytes(), data_content:float=None) -> None:
        
        assert ((bytes_content != b"") or (data_content is not None))\
            , "Either bytes_content or data_content must be provided."
        
        
        self.bytes_content = bytes_content
        self.data_content = data_content
        
        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content is None:
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data:float) -> bytes:
        scaled = int(round(data * (1 << 5)))  # 乘以 32
        if not -(1 << 31) <= scaled < (1 << 31):
            raise ValueError("Value out of range for 32-bit signed fixed-point")
        return scaled.to_bytes(4, byteorder='big', signed=True)
    

    def data_decode(self, data: bytes) -> float:
        """
        Decode 4-byte big-endian Q27.5 fixed-point bytes into float.
        """
        if len(data) != 4:
            raise ValueError("Expected 4 bytes for Q27.5 fixed-point data")
        
        fixed = int.from_bytes(data, byteorder='big', signed=True)
        return fixed / (1 << 5)  # 等价于除以 32

