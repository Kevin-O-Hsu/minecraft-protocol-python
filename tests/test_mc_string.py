import unittest
from src.data_struct import McString
from src.data_struct import McVarInt

class TestMcString(unittest.TestCase):
    
    def test_init(self):
        # breakpoint()
        s = McString(data_content="Hello, World!")
        self.assertEqual(s.data_content, "Hello, World!")
        self.assertEqual(s.bytes_content.hex().lstrip('0'), hex(13).lstrip("0x") + b'Hello, World!'.hex())
        print(s.bytes_content.hex().lstrip('0'))
        
    def test_decode(self):
        text = "Hello, World!"
        encoded = McVarInt(data_content=len(text.encode("utf-8"))).bytes_content + text.encode("utf-8")
        self.assertEqual(McString(bytes_content=encoded).data_content, text)
    