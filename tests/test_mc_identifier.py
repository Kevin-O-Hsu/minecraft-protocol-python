import unittest
from src.data_struct import McIdentifier


class TestMcIdentifier(unittest.TestCase):

    def test_encode_identifier(self):
        identifier = ("minecraft", "stone")
        obj = McIdentifier(data_content=identifier)

        # 将字节转成 hex string 输出用于调试
        hex_str = obj.bytes_content.hex()
        print(obj.bytes_content)  # 原始 bytes
        print(hex_str)            # 十六进制

        # UTF-8编码后的 "minecraft:stone"
        expected_suffix = "6d696e6563726166743a73746f6e65"
        self.assertTrue(hex_str.endswith(expected_suffix))
        self.assertEqual(obj.data_content, identifier)


    def test_decode_identifier(self):
        raw = b'\x10minecraft:stone'
        obj = McIdentifier(bytes_content=raw)
        self.assertEqual(obj.data_content, ("minecraft", "stone"))
        self.assertEqual(obj.bytes_content, raw)

    def test_invalid_both_inputs(self):
        with self.assertRaises(ValueError) as cm:
            McIdentifier(bytes_content=b'\x01', data_content=("abc", "def"))
        self.assertIn("provide exactly one", str(cm.exception))

    def test_invalid_both_empty(self):
        with self.assertRaises(ValueError):
            McIdentifier()

    def test_invalid_namespace_characters(self):
        with self.assertRaises(ValueError) as cm:
            McIdentifier(data_content=("MineCraft!", "stone"))
        self.assertIn("Invalid namespace", str(cm.exception))

    def test_invalid_value_characters(self):
        with self.assertRaises(ValueError) as cm:
            McIdentifier(data_content=("minecraft", "sto@ne"))
        self.assertIn("Invalid identifier value", str(cm.exception))

    def test_decode_complex_identifier(self):
        obj = McIdentifier(data_content=("my_mod", "block/type_1"))
        re_encoded = McIdentifier(bytes_content=obj.bytes_content)
        self.assertEqual(re_encoded.data_content, ("my_mod", "block/type_1"))

