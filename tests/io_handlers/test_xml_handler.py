#!/usr/bin/env python
import unittest
from StringIO import StringIO
from tempfile import NamedTemporaryFile

from life_game.models.state import State
from life_game.models.organism import Organism
from life_game.io_handlers.xml_handler import XMLHandlerMixin, XMLFileError

 
class TestXMLHandlerMixin(unittest.TestCase):
 
    def setUp(self):
        self.xml_string = """<?xml version="1.0" encoding="UTF-8"?><life><world><cells>5</cells>
            <species>3</species><iterations>3</iterations></world><organisms><organism><x_pos>
            0</x_pos><y_pos>0</y_pos><species>2</species></organism><organism><x_pos>1</x_pos>
            <y_pos>0</y_pos><species>2</species></organism><organism><x_pos>4</x_pos><y_pos>
            0</y_pos><species>1</species></organism><organism><x_pos>0</x_pos><y_pos>1</y_pos>
            <species>2</species></organism><organism><x_pos>2</x_pos><y_pos>1</y_pos><species>1
            </species></organism><organism><x_pos>3</x_pos><y_pos>1</y_pos><species>1</species>
            </organism></organisms></life>"""
        self.input_file = StringIO(self.xml_string)

        self.xml_handler = XMLHandlerMixin()

    def test_read_state_from_xml_success(self):
        state = self.xml_handler.read_state_from_xml(self.input_file)

        self.assertEqual(state.cells_cnt, 5)
        self.assertEqual(state.species_cnt, 3)
        self.assertEqual(state.iterations_cnt, 3)

        self.assertEqual(len(state.organism_l), 6)

        organism = state.organism_l[0]
        self.assertEqual(organism.x, 0)
        self.assertEqual(organism.y, 0)
        self.assertEqual(organism.species, 2)

    def test_read_state_from_xml_not_valid(self):
        self.xml_string = self.xml_string[:20]
        self.input_file = StringIO(self.xml_string)

        with self.assertRaises(XMLFileError):
            self.xml_handler.read_state_from_xml(self.input_file)

    def test_read_state_from_xml_elements_with_not_value(self):
        self.xml_string = """<?xml version="1.0" encoding="UTF-8"?><life><world><cells></cells>
            </world></life>"""
        self.input_file = StringIO(self.xml_string)

        with self.assertRaises(XMLFileError):
            self.xml_handler.read_state_from_xml(self.input_file)

    def test_read_state_from_xml_wrong_elements(self):
        self.xml_string = """<?xml version="1.0" encoding="UTF-8"?><life><world><cat>1</cat>
            </world></life>"""
        self.input_file = StringIO(self.xml_string)

        with self.assertRaises(XMLFileError):
            self.xml_handler.read_state_from_xml(self.input_file)

    def test_write_state_to_xml_success(self):
        original_state = State(5, 4, 3, [Organism(3, 2, 1), Organism(3, 1, 2)])

        # test with temp file should be enough
        with NamedTemporaryFile(delete=False) as test_write_file:
            self.xml_handler.write_state_to_xml(test_write_file, original_state, 3)

        with open(test_write_file.name, 'r') as test_read_file:
            state = self.xml_handler.read_state_from_xml(test_read_file)

            self.assertEqual(state.cells_cnt, original_state.cells_cnt)
            self.assertEqual(state.species_cnt, original_state.species_cnt)
            self.assertEqual(state.iterations_cnt, original_state.iterations_cnt)

    def test_write_state_to_xml_file_does_not_exist(self):
        state = State(5, 4, 3, [Organism(3, 2, 1), Organism(3, 1, 2)])

        output_file = '/note/existing/nofile.xml'

        with self.assertRaises(XMLFileError):
            self.xml_handler.write_state_to_xml(output_file, state, 1)
