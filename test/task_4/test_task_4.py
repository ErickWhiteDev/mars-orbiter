import unittest
import subprocess
import sys
import hashlib

class TestTask4(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_4"])

    def test_N_omega_RnN(self):
        expected_file = "test/task_4/N_omega_RnN.txt"
        output_file = "output/task_4/N_omega_RnN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_RnN(self):
        expected_file = "test/task_4/RnN.txt"
        output_file = "output/task_4/RnN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())
                