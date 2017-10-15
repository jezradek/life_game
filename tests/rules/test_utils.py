#!/usr/bin/env python
import unittest

from life_game.models.organism import Organism
from life_game.rules.utils import get_occurence_dict_by_attr
 

class TestUtils(unittest.TestCase):
 
    def setUp(self):
        self.organism_l = [Organism(0, 2, 1), Organism(-1, 2, 1), Organism(1, -3, 1),
            Organism(-1, -5, 1), Organism(10, 2, 2), Organism(2, 20, 2)]

    def test_get_occurence_dict_by_attr_species_success(self):
        species_occurrence_d = get_occurence_dict_by_attr(self.organism_l, 'species')

        self.assertEqual(species_occurrence_d[1], 4)
        self.assertEqual(species_occurrence_d[2], 2)

    def test_get_occurence_dict_by_attr_x_success(self):
        species_occurrence_d = get_occurence_dict_by_attr(self.organism_l, 'x')

        self.assertEqual(species_occurrence_d[-1], 2)
        self.assertEqual(len(species_occurrence_d), 5)

    def test_get_occurence_dict_by_attr_species_with_none_elements_success(self):
        self.organism_l += [None, None, None]
        species_occurrence_d = get_occurence_dict_by_attr(self.organism_l, 'species')

        self.assertEqual(species_occurrence_d[1], 4)
        self.assertEqual(species_occurrence_d[2], 2)

    def test_get_occurence_dict_by_attr_with_none_elements(self):
        self.organism_l = [None, None, None]
        species_occurrence_d = get_occurence_dict_by_attr(self.organism_l, 'species')

        # species occurence dict will be empty
        self.assertFalse(species_occurrence_d)
