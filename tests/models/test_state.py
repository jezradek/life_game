#!/usr/bin/env python
import unittest

from life_game.models.state import State
from life_game.models.organism import Organism


class TestState(unittest.TestCase):

    def test_state_is_valid(self):
        state = State(5, 4, 3, [Organism(3, 2, 1), Organism(3, 1, 2)])
        state_final = State(5, 4, 0, [Organism(3, 2, 1), Organism(3, 1, 2)])

        self.assertTrue(state.is_valid())
        self.assertTrue(state_final.is_valid())

    def test_state_is_not_valid(self):
        # missing attributes
        state_without_organisms = State(5, 4, 3, None)
        state_without_species = State(5, 4, None, None)

        self.assertFalse(state_without_organisms.is_valid())
        self.assertFalse(state_without_species.is_valid())
