import unittest
import subprocess
import sys
import hashlib

class TestTask11(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_11"])

    def test_mrp_300(self):
        expected_file = "test/task_11/mrp_300.txt"
        output_file = "output/task_11/mrp_300.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_mrp_2100(self):
        expected_file = "test/task_11/mrp_2100.txt"
        output_file = "output/task_11/mrp_2100.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_mrp_3400(self):
        expected_file = "test/task_11/mrp_3400.txt"
        output_file = "output/task_11/mrp_3400.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_mrp_4400(self):
        expected_file = "test/task_11/mrp_4400.txt"
        output_file = "output/task_11/mrp_4400.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_mrp_5600(self):
        expected_file = "test/task_11/mrp_5600.txt"
        output_file = "output/task_11/mrp_5600.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())
