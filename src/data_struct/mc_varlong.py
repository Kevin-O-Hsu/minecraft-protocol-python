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


class McVarLong(McDataStruct):

    def __init__(
        self, *, bytes_content: bytes = bytes(), data_content: int = None
    ) -> None:
        """
        VarLongs are never longer than 10 bytes.
        Variable-length format such that smaller numbers use fewer bytes.
        These are very similar to Protocol Buffer Varints:
        the 7 least significant bits are used to encode the value and the most significant bit indicates whether there's another byte after it for the next part of the number.
        The least significant group is written first,
        followed by each of the more significant groups;
        thus, VarInts are effectively little endian (however, groups are 7 bits, not 8).
        """
        # Ensure that at least one of bytes_content or data_content is provided
        assert (bytes_content != b"") or (
            data_content is not None
        ), "Either bytes_content or data_content must be provided."

        self.bytes_content = bytes_content
        self.data_content = data_content

        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content is None:
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data: int) -> bytes:
        """Encodes an integer to Minecraft VarLong format (max 10 bytes)."""
        result = bytearray()
        for _ in range(10):
            temp = data & 0x7F  # Get the lowest 7 bits
            data >>= 7
            if data != 0:
                result.append(temp | 0x80)  # Set continuation bit
            else:
                result.append(temp)
                return bytes(result)
        raise ValueError("VarLong is too big (more than 10 bytes)")

    def data_decode(self, data: bytes) -> int:
        """Decodes a Minecraft VarLong from bytes."""
        result = 0
        shift = 0
        for byte in data:
            result |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:  # If the continuation bit is 0, we're done
                break
            shift += 7
        else:
            raise ValueError("VarLong is too big (more than 10 bytes)")
        return result

    def decode_varlong_with_size(self, data: bytes) -> tuple[int, int]:
        """
        Decode a Minecraft-style Long from bytes and return (value, bytes_used).
        """
        num_read = 0
        result = 0
        for i in range(min(10, len(data))):
            byte = data[i]
            result |= (byte & 0x7F) << (7 * i)
            num_read += 1
            if (byte & 0x80) == 0:
                return result, num_read
        raise ValueError("VarLong is too long or incomplete")
