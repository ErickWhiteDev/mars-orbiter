import unittest
import subprocess
import sys

class TestTask3(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_3"])

    def test_N_omega_RsN(self):
        expected_file = "test/task_3/N_omega_RsN.txt"
        output_file = "output/task_3/N_omega_RsN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'r') as output:
                self.assertEqual(output.read(), expected.read())

    def test_RsN(self):
        expected_file = "test/task_3/RsN.txt"
        output_file = "output/task_3/RsN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'r') as output:
                self.assertEqual(output.read(), expected.read())
                