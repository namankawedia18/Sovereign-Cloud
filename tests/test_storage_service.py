import os
import tempfile
import unittest
from io import BytesIO

from services import storage_service


class StorageServiceAzureAwareTests(unittest.TestCase):
    def test_local_save_and_read_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, "demo.txt")
            uploaded = BytesIO(b"hello azure")
            uploaded.filename = "demo.txt"

            storage_service.save_file(uploaded, file_path)

            self.assertTrue(storage_service.file_exists(file_path))
            self.assertEqual(storage_service.read_file_bytes(file_path), b"hello azure")

            storage_service.delete_file(file_path)
            self.assertFalse(storage_service.file_exists(file_path))


if __name__ == "__main__":
    unittest.main()
