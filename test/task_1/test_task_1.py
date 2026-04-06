import unittest
import subprocess
import sys
import hashlib

class TestTask1(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_1"])

    def test_r_LMO(self):
        expected_file = "test/task_1/r_LMO.txt"
        output_file = "output/task_1/r_LMO.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_v_LMO(self):
        expected_file = "test/task_1/v_LMO.txt"
        output_file = "output/task_1/v_LMO.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_r_GMO(self):
        expected_file = "test/task_1/r_GMO.txt"
        output_file = "output/task_1/r_GMO.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_v_GMO(self):
        expected_file = "test/task_1/v_GMO.txt"
        output_file = "output/task_1/v_GMO.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())
                