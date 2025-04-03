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
    def __init__(
        self,
        *,
        bytes_content: bytes = bytes(),
        data_content: tuple[str, str] = tuple(),
    ) -> None:
        """
        data_content: (namespace, value)
        """
        if bool(bytes_content) + bool(data_content) != 1:
            raise ValueError(
                "You must provide exactly one of bytes_content or data_content."
            )

        if data_content:
            namespace, value = data_content
            if not re.fullmatch(r"[a-z0-9._-]+", namespace):
                raise ValueError(f"Invalid namespace: {namespace}")
            if not re.fullmatch(r"[a-z0-9._/\-]+", value):
                raise ValueError(f"Invalid identifier value: {value}")

        self.bytes_content = bytes_content
        self.data_content = data_content

        if not self.bytes_content:
            self.bytes_content = self.data_encode(self.data_content)
        else:
            self.data_content = self.data_decode(self.bytes_content)

    def data_encode(self, data: tuple[str, str]) -> bytes:
        """
        Encode the Identifier as a Minecraft VarInt-prefixed UTF-8 string.
        Format: namespace:value
        """
        namespace, value = data
        full_string = f"{namespace}:{value}"
        utf8_bytes = full_string.encode("utf-8")
        length_bytes = McVarInt(data_content=len(utf8_bytes)).bytes_content
        return length_bytes + utf8_bytes

    def data_decode(self, data: bytes) -> tuple[str, str]:
        """
        Decode a Minecraft VarInt-prefixed UTF-8 string back into an Identifier (namespace:value).
        """
        length, length_size = McVarInt(bytes_content=data).decode_varint_with_size()
        str_bytes = data[length_size : length_size + length]
        decoded_string = str_bytes.decode("utf-8")
        namespace, value = decoded_string.split(":", 1)
        return (namespace, value)
