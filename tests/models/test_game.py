#!/usr/bin/env python
import os
import unittest

from life_game.models.game import Game, GameRuntimeError
from life_game.models.state import State
from life_game.models.organism import Organism
from life_game.io_handlers.game_io_handler import GameIOHandler


class TestGame(unittest.TestCase):
    OUT_FILE = 'test-out.xml'
 
    def setUp(self):
        self.original_organism_l = [
            Organism(2, 0, 1), Organism(1, 1, 1), Organism(2, 1, 1), Organism(3, 1, 2),
            Organism(1, 2, 2), Organism(2, 2, 2), Organism(3, 2, 2), Organism(0, 3, 2),
            Organism(1, 3, 2), Organism(3, 3, 2)
        ]
        self.initial_state = State(5, 2, 2, self.original_organism_l)
        # we set out file as input file in order to check final state of the game
        self.io_handler = GameIOHandler('dummy.xml', self.OUT_FILE)

        self.game = Game(self.io_handler, self.initial_state)

    def test_start_success(self):
        self.game.start()

        state = self.io_handler.read_state(self.OUT_FILE)

        self.assertEqual(state.cells_cnt, self.initial_state.cells_cnt)
        self.assertEqual(state.species_cnt, self.initial_state.species_cnt)
        self.assertEqual(state.iterations_cnt, 0)
        self.assertEqual(len(state.organism_l), 14)
        # tests for concrete organisms are in test_world.py

    def test_start_not_existing_organisms_provided(self):
        self.initial_state.organism_l = [Organism(100, -20, 1), Organism(1, -10, 2)]
        self.game = Game(self.io_handler, self.initial_state)

        with self.assertRaises(GameRuntimeError):
            self.game.start()

    def tearDown(self):
        try:
            os.remove(self.OUT_FILE)
        except (OSError, IOError) as err:
            print 'Can not remove test file: %s' % err.message
