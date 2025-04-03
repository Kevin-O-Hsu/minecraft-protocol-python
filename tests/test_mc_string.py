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


import unittest
from src.data_struct import McString
from src.data_struct import McVarInt


class TestMcString(unittest.TestCase):

    def test_init(self):
        # breakpoint()
        s = McString(data_content="Hello, World!")
        self.assertEqual(s.data_content, "Hello, World!")
        self.assertEqual(
            s.bytes_content.hex().lstrip("0"),
            hex(13).lstrip("0x") + b"Hello, World!".hex(),
        )
        print(s.bytes_content.hex().lstrip("0"))

    def test_decode(self):
        text = "Hello, World!"
        encoded = McVarInt(
            data_content=len(text.encode("utf-8"))
        ).bytes_content + text.encode("utf-8")
        self.assertEqual(McString(bytes_content=encoded).data_content, text)
