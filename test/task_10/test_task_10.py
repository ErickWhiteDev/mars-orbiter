import unittest
import subprocess
import sys
import hashlib

class TestTask10(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_10"])

    def test_mrp_15(self):
        expected_file = "test/task_10/mrp_15.txt"
        output_file = "output/task_10/mrp_15.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_mrp_100(self):
        expected_file = "test/task_10/mrp_100.txt"
        output_file = "output/task_10/mrp_100.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_mrp_200(self):
        expected_file = "test/task_10/mrp_200.txt"
        output_file = "output/task_10/mrp_200.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_mrp_400(self):
        expected_file = "test/task_10/mrp_400.txt"
        output_file = "output/task_10/mrp_400.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())
