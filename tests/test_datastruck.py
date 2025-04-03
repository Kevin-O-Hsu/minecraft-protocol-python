import unittest
from src.data_struct import McDataStruct


class MockMcDataStruct(McDataStruct):
    def data_decode(self, bytes_content: bytes) -> tuple:
        return tuple(bytes_content)

    def data_encode(self, data_content: tuple) -> bytes:
        return bytes(data_content)


class TestMcDataStruct(unittest.TestCase):

    def test_encode_from_data_content(self):
        data = (1, 2, 3)
        obj = MockMcDataStruct(data_content=data)
        self.assertEqual(obj.data_content, data)
        self.assertEqual(obj.bytes_content, b"\x01\x02\x03")

    def test_decode_from_bytes_content(self):
        byte_data = b"\x04\x05\x06"
        obj = MockMcDataStruct(bytes_content=byte_data)
        self.assertEqual(obj.bytes_content, byte_data)
        self.assertEqual(obj.data_content, (4, 5, 6))

    def test_raises_if_both_empty(self):
        with self.assertRaises(ValueError) as cm:
            MockMcDataStruct()
        self.assertIn("provide exactly one", str(cm.exception))

    def test_raises_if_both_given(self):
        with self.assertRaises(ValueError) as cm:
            MockMcDataStruct(bytes_content=b"\x01", data_content=(1,))
        self.assertIn("provide exactly one", str(cm.exception))

    def test_pass_only_data_content(self):
        obj = MockMcDataStruct(data_content=(10, 20))
        self.assertEqual(obj.bytes_content, b"\x0a\x14")
        self.assertEqual(obj.data_content, (10, 20))

    def test_pass_only_bytes_content(self):
        obj = MockMcDataStruct(bytes_content=b"\xff")
        self.assertEqual(obj.data_content, (255,))
        self.assertEqual(obj.bytes_content, b"\xff")
