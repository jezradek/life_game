#!/usr/bin/env python
import os
import unittest
from StringIO import StringIO

from life_game.models.state import State
from life_game.models.organism import Organism
from life_game.io_handlers.game_io_handler import GameIOHandler, IOValidationError, \
    ReadStateError


class TestGameIOHandler(unittest.TestCase):
    OUT_FILE = 'test-ioout.xml'
 
    def setUp(self):
        self.xml_string = """<?xml version="1.0" encoding="UTF-8"?><life><world><cells>5</cells>
            <species>3</species><iterations>3</iterations></world><organisms><organism><x_pos>0</x_pos>
            <y_pos>0</y_pos><species>2</species></organism><organism><x_pos>1</x_pos><y_pos>0</y_pos>
            <species>2</species></organism><organism><x_pos>4</x_pos><y_pos>0</y_pos><species>1</species>
            </organism><organism><x_pos>0</x_pos><y_pos>1</y_pos><species>2</species></organism><organism>
            <x_pos>2</x_pos><y_pos>1</y_pos><species>1</species></organism><organism><x_pos>3</x_pos>
            <y_pos>1</y_pos><species>1</species></organism></organisms></life>"""
        self.input_file = StringIO(self.xml_string)

        self.io_handler = GameIOHandler(self.input_file, self.OUT_FILE, keep_out_file_open=False)

        self.original_state = State(5, 4, 3, [Organism(3, 2, 1), Organism(3, 1, 2)])
 
    def test_check_input_success(self):
        original_file = 'samples/test.xml'
        arguments = ['run.py', 'samples/test.xml']

        input_file = GameIOHandler.check_input(arguments)

        self.assertEqual(input_file, original_file)

    def test_check_input_file_wrong_number_of_arguments(self):
        arguments = ['run.py', 'test.xml', 'extra_argument']

        with self.assertRaises(IOValidationError):
            input_file = GameIOHandler.check_input(arguments)

    def test_check_input_file_does_not_exist(self):
        original_file = 'not-existing.xml'
        arguments = ['run.py', original_file]

        with self.assertRaises(IOValidationError):
            input_file = GameIOHandler.check_input(arguments)

    def test_usage_success_default_message(self):
        info = '! Execute: <python run.py input_file.xml> in order to run the game.\n! ' \
            'Error: The input XML file must be specified.'
        message = GameIOHandler.usage()

        self.assertEqual(message, info)

    def test_usage_success_custom_message(self):
        info = 'Test'
        info_test = '! Execute: <python run.py input_file.xml> in order to run the game.\n! ' \
            'Error: %s' % info
        message = GameIOHandler.usage(info)

        self.assertEqual(message, info_test)

    def test_read_state_success(self):
        state = self.io_handler.read_state()

        self.assertTrue(state)
        # no need to check all arguments as we did in the XML handler tests

    def test_read_state_not_valid(self):
        self.xml_string = """<?xml version="1.0" encoding="UTF-8"?><life><world>
            <species>3</species></world><organisms></organisms></life>"""
        self.input_file = StringIO(self.xml_string)

        self.io_handler = GameIOHandler(self.input_file)

        with self.assertRaises(ReadStateError):
            state = self.io_handler.read_state()

    def test_read_state_not_valid(self):
        self.xml_string = """<?xml version="1.0" encoding="UTF-8"?><life><world><cat>1</cat>
            </world></life>"""
        self.input_file = StringIO(self.xml_string)

        self.io_handler = GameIOHandler(self.input_file, keep_out_file_open=False)

        with self.assertRaises(ReadStateError):
            state = self.io_handler.read_state()

    def test_write_state_success(self):
        self.io_handler.opened_output_file = self.io_handler._open_file()

        self.io_handler.write_state(self.original_state, 5)
        self.io_handler.clean()

        state = self.io_handler.read_state(self.OUT_FILE)

        self.assertEqual(state.cells_cnt, self.original_state.cells_cnt)
        self.assertEqual(state.species_cnt, self.original_state.species_cnt)
        self.assertEqual(state.iterations_cnt, 5)
        self.assertEqual(len(state.organism_l), 2)

        self.clean()

    def clean(self):
        try:
            os.remove(self.OUT_FILE)
        except (OSError, IOError) as err:
            print 'Can not remove test file: %s' % err.message
