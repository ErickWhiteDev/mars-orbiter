import unittest
import subprocess
import sys
import hashlib

class TestTask6(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_6"])

    def test_B_omega_BRs(self):
        expected_file = "test/task_6/B_omega_BRs.txt"
        output_file = "output/task_6/B_omega_BRs.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_sigma_BRs(self):
        expected_file = "test/task_6/sigma_BRs.txt"
        output_file = "output/task_6/sigma_BRs.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_B_omega_BRn(self):
        expected_file = "test/task_6/B_omega_BRn.txt"
        output_file = "output/task_6/B_omega_BRn.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_sigma_BRn(self):
        expected_file = "test/task_6/sigma_BRn.txt"
        output_file = "output/task_6/sigma_BRn.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_B_omega_BRc(self):
        expected_file = "test/task_6/B_omega_BRc.txt"
        output_file = "output/task_6/B_omega_BRc.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())

    def test_sigma_BRc(self):
        expected_file = "test/task_6/sigma_BRc.txt"
        output_file = "output/task_6/sigma_BRc.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'rb') as output:
            self.assertEqual(hashlib.file_digest(output, "sha256").hexdigest(), expected.read().strip())
