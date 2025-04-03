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
from .mc_array import McArray


class McFixedArray(McDataStruct):

    def __init__(
        self,
        *,
        bytes_content: bytes = bytes(),
        data_content: tuple[McVarInt, McArray] = None
    ) -> None:
        """
        data_content: (length: McVarInt, data: McArray)
        Represents an array prefixed by its length. If the array is empty the length will still be encoded.
        """
        assert True in [
            bool(item) for item in (bytes_content, data_content)
        ], "Either bytes_content or data_content must be provided"

        self.bytes_content = bytes_content
        self.data_content = data_content

        if (self.bytes_content == bytes()) and (self.data_content is not None):
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content is None:
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data: tuple[McVarInt, McArray]) -> bytes:
        """
        Encode a prefixed array: [VarInt(length) + array bytes]
        """
        length_bytes = data[0].bytes_content  # McVarInt
        array_bytes = data[1].bytes_content  # McArray
        return length_bytes + array_bytes

    def data_decode(self, data: bytes) -> tuple[McVarInt, McArray]:
        """
        Decode a prefixed array from bytes.
        """
        # 解码前缀长度
        length, length_size = McVarInt(bytes_content=data).decode_varint_with_size()

        # 解码数组内容
        array_bytes = data[length_size:]
        array = McArray(bytes_content=array_bytes, count=length)

        return McVarInt(data_content=length), array
