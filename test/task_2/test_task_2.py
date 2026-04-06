import unittest
import subprocess
import sys

class TestTask2(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.run([sys.executable, "-m", "tasks.task_2"])

    def test_HN(self):
        expected_file = "test/task_2/HN.txt"
        output_file = "output/task_2/HN.txt"

        with open(expected_file, 'r') as expected, open(output_file, 'r') as output:
                self.assertEqual(output.read(), expected.read())
                