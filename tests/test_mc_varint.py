import unittest
from src.data_struct import McVarInt


class TestMcVarInt(unittest.TestCase):

    def test_encode_varint(self):
        data = 12345
        obj = McVarInt(data_content=data)
        encoded = obj.bytes_content

        # 重新实例化，确认编码的字节是否能正确解码回原始数字
        obj2 = McVarInt(bytes_content=encoded)
        self.assertEqual(obj2.data_content, data)

        # 对应的小端编码应该是 "31d4"

        tests = [
            (0, "00"),
            (1, "01"),
            (2, "02"),
            (127, "7f"),
            (128, "8001"),
            (255, "ff01"),
            (25565, "ddc701"),
            (2097151, "ffff7f"),
            (2147483647, "ffffffff07"),
            (-1, "ffffffff0f"),
            (-2147483648, "8080808008"),
        ]

        for number, expected_hex in tests:
            test_obj = McVarInt(data_content=number)
            # print(number, expected_hex)
            # print(test_obj.bytes_content)
            self.assertEqual(test_obj.bytes_content.hex(), expected_hex)

    def test_decode_varint(self):
        tests = [
            (0, "00"),
            (1, "01"),
            (2, "02"),
            (127, "7f"),
            (128, "8001"),
            (255, "ff01"),
            (25565, "ddc701"),
            (2097151, "ffff7f"),
            (2147483647, "ffffffff07"),
            (-1, "ffffffff0f"),
            (-2147483648, "8080808008"),
        ]
        for expected_number, input_hex in tests:
            print(expected_number, input_hex)

            test_obj = McVarInt(bytes_content=bytes.fromhex(input_hex))
            self.assertEqual(test_obj.data_content, expected_number)

    def test_invalid_both_empty(self):
        with self.assertRaises(ValueError) as cm:
            McVarInt()
        self.assertIn(
            "You must provide exactly one of bytes_content or data_content.",
            str(cm.exception),
        )

    def test_invalid_both_given(self):
        with self.assertRaises(ValueError) as cm:
            McVarInt(bytes_content=b"\x01", data_content=123)
        self.assertIn(
            "You must provide exactly one of bytes_content or data_content.",
            str(cm.exception),
        )

    def test_varint_too_large(self):
        large_number = 2**35
        with self.assertRaises(ValueError) as cm:
            McVarInt(data_content=large_number)
        self.assertIn("VarInt is too big (more than 5 bytes)", str(cm.exception))

    def test_varint_incomplete(self):
        incomplete_varint = bytes([0x80])  # Only part of a VarInt encoding
        with self.assertRaises(ValueError) as cm:
            McVarInt(bytes_content=incomplete_varint)
        self.assertIn("VarInt is too big (more than 5 bytes)", str(cm.exception))

    # def test_varint_decode_with_size(self):
    #     encoded = bytes([0x31, 0xd4])  # 小端编码
    #     obj = McVarInt(bytes_content=encoded)
    #     result, size = obj.decode_varint_with_size()
    #     self.assertEqual(result, 12345)
    #     self.assertEqual(size, 2)
