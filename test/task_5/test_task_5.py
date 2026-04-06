import unittest
import subprocess
import sys

class TestTask5(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_5"])

    def test_N_omega_RcN(self):
        expected_file = "test/task_5/N_omega_RcN.txt"
        output_file = "output/task_5/N_omega_RcN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'r') as output:
                self.assertEqual(output.read(), expected.read())

    def test_RcN(self):
        expected_file = "test/task_5/RcN.txt"
        output_file = "output/task_5/RcN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'r') as output:
                self.assertEqual(output.read(), expected.read())
                