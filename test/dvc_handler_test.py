import os
import unittest

from src.dvc.dvc_handler import change_file


class TestChangeFileFunction(unittest.TestCase):

    def setUp(self):
        self.data_path = "test_file.txt"
        self.version = "1.0"

    def test_change_file_with_string_version(self):
        change_file(self.data_path, self.version)
        with open(self.data_path, "r") as myfile:
            content = myfile.read()
            self.assertTrue(f"appended text - {self.version}" in content)

    def test_change_file_file_exists(self):
        if os.path.exists(self.data_path):
            os.remove(self.data_path)
        change_file(self.data_path, self.version)
        self.assertTrue(os.path.exists(self.data_path))


if __name__ == '__main__':
    unittest.main()
