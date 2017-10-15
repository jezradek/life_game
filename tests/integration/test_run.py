#!/usr/bin/env python
import unittest
import subprocess


class TestRun(unittest.TestCase):
    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1

    def test_run_success(self):
        exit_status = subprocess.call(['python', 'run.py', 'samples/test.xml'])

        self.assertEqual(exit_status, self.EXIT_SUCCESS)

    def test_run_wrong_number_of_arguments(self):
        exit_status = subprocess.call(['python', 'run.py', 'samples/test.xml', 'extra_argument'])

        self.assertEqual(exit_status, self.EXIT_FAILURE)

    def test_run_file_does_not_exist(self):
        exit_status = subprocess.call(['python', 'run.py', 'non_existing.xml'])

        self.assertEqual(exit_status, self.EXIT_FAILURE)
        # tests for exact messages are int test_game_io_handler.py
