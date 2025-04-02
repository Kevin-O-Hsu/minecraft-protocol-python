import unittest
from src.data_struct.mc_string import McString


class TestMcString(unittest.TestCase):
    
    def test_init(self):
        # breakpoint()
        s = McString(data_content="Hello, World!")
        self.assertEqual(s.data_content, "Hello, World!")
        self.assertEqual(s.bytes_content.hex().lstrip('0'), hex(13).lstrip("0x") + b'Hello, World!'.hex())
        print(s.bytes_content.hex())   

    