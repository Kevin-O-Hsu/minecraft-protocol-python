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
    
    def __init__(self, *,  bytes_content:bytes = bytes(), data_content:int = None) -> None:
        # Ensure that at least one of bytes_content or data_content is provided
        assert ((bytes_content != b"") or (data_content is not None)), "Either bytes_content or data_content must be provided."
        
        self.bytes_content = bytes_content
        self.data_content = data_content
        
        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content is None:
            self.data_content = self.data_decode(self.bytes_content)
    
    def data_encode(self, data: int) -> bytes:
        """Encodes an integer to Minecraft VarInt format (max 5 bytes)."""
        result = bytearray()
        for _ in range(5):
            temp = data & 0x7F  # Get the lowest 7 bits
            data >>= 7
            if data != 0:
                result.append(temp | 0x80)  # Set continuation bit
            else:
                result.append(temp)
                return bytes(result)
        raise ValueError("VarInt is too big (more than 5 bytes)")

    def data_decode(self, data: bytes) -> int:
        """Decodes a Minecraft VarInt from bytes."""
        result = 0
        shift = 0
        for byte in data:
            result |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:  # If the continuation bit is 0, we're done
                break
            shift += 7
        else:
            raise ValueError("VarInt is too big (more than 5 bytes)")
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