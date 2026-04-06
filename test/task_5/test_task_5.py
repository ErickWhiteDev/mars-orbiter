import unittest
import subprocess
import sys
import hashlib

class TestTask5(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_5"])

    def test_N_omega_RcN(self):
        expected_file = "test/task_5/N_omega_RcN.txt"
        output_file = "output/task_5/N_omega_RcN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_RcN(self):
        expected_file = "test/task_5/RcN.txt"
        output_file = "output/task_5/RcN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())
                