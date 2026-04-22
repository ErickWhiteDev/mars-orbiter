import unittest
import subprocess
import sys
import hashlib

class TestTask7(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_7"])

    def test_B_H(self):
        expected_file = "test/task_7/B_H.txt"
        output_file = "output/task_7/B_H.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_T(self):
        expected_file = "test/task_7/T.txt"
        output_file = "output/task_7/T.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_zero_mrp(self):
        expected_file = "test/task_7/zero_mrp.txt"
        output_file = "output/task_7/zero_mrp.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_N_H(self):
        expected_file = "test/task_7/N_H.txt"
        output_file = "output/task_7/N_H.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_const_mrp(self):
        expected_file = "test/task_7/const_mrp.txt"
        output_file = "output/task_7/const_mrp.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())
