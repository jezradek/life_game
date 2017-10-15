#!/usr/bin/env python
import unittest

from life_game.models.organism import Organism
from life_game.models.world_grid import WorldGrid
from life_game.models.world import World, WorldInternalError
from life_game.rules.evolution_rules_engine import EvolutionRulesEngine


class TestWorld(unittest.TestCase):
 
    def setUp(self):
        world_grid = WorldGrid(5, 5)
        self.original_organism_l = [
            Organism(2, 0, 1), Organism(1, 1, 1), Organism(2, 1, 1), Organism(3, 1, 2),
            Organism(1, 2, 2), Organism(2, 2, 2), Organism(3, 2, 2), Organism(0, 3, 2),
            Organism(1, 3, 2), Organism(3, 3, 2)
        ]

        rules_engine = EvolutionRulesEngine()

        self.world = World(world_grid, self.original_organism_l, rules_engine)

    def test_height(self):
        self.assertEqual(self.world.height, 5)
 
    def test_width(self):
        self.assertEqual(self.world.width, 5)

    def test_populate_with_organisms_success(self):
        initial_conflict = self.world.populate_initial_organisms()

        self.assertFalse(initial_conflict)
        self.assertEqual(len(self.world.organism_l), 10)
        self.assertEqual(len(self.world._get_all_organisms()), 10)

    def test_populate_with_organisms_two_occupy_same_element(self):
        # if two organisms occupy same element, one of them must die
        organism_l = [Organism(1, 1, 1), Organism(1, 1, 2), Organism(2, 2, 2)]
        self.world.organism_l = organism_l
        initial_conflict = self.world.populate_initial_organisms()

        self.assertTrue(initial_conflict)
        self.assertEqual(len(self.world.organism_l), 2)
        self.assertEqual(len(self.world._get_all_organisms()), 2)

    def test_populate_with_organisms_more_occupy_same_element(self):
        # if more organisms occupy same element, only lucky one will live on
        organism_l = [Organism(1, 1, 1), Organism(1, 1, 2), Organism(2, 2, 2),
            Organism(2, 2, 2), Organism(2, 2, 2), Organism(2, 2, 2)]
        self.world.organism_l = organism_l
        initial_conflict = self.world.populate_initial_organisms()

        self.assertTrue(initial_conflict)
        self.assertEqual(len(self.world.organism_l), 2)
        self.assertEqual(len(self.world._get_all_organisms()), 2)

    def test_populate_with_organisms_not_existing_organisms_provided(self):
        # if more organisms occupy same element, only lucky one will live on
        organism_l = [Organism(100, -20, 1), Organism(1, -10, 2)]
        self.world.organism_l = organism_l

        with self.assertRaises(WorldInternalError):
            self.world.populate_initial_organisms()

    def test_iterate_success(self):
        self.world.populate_initial_organisms()
        self.world.iterate()

        self.assertNotEqual(self.world.organism_l, self.original_organism_l)
        self.assertEqual(len(self.world.organism_l), 12)
        self.assertEqual(len(self.world._get_all_organisms()), 12)

        # checking born ones
        organism_species_1 = self.world._get_organism_at(1, 0)
        self.assertTrue(organism_species_1)
        self.assertEqual(organism_species_1.species, 1)
        self.assertTrue(self.world._get_organism_at(0, 2))
        self.assertTrue(self.world._get_organism_at(4, 2))
        # checking some of survived ones
        self.assertTrue(self.world._get_organism_at(0, 2))
        self.assertTrue(self.world._get_organism_at(3, 1))
        # checking dead one
        self.assertFalse(self.world._get_organism_at(2, 2))

    def test_iterate_two_times_success(self):
        self.world.populate_initial_organisms()
        self.world.iterate()
        self.world.iterate()

        self.assertNotEqual(self.world.organism_l, self.original_organism_l)
        self.assertEqual(len(self.world.organism_l), 14)
        self.assertEqual(len(self.world._get_all_organisms()), 14)

        # checking born ones
        organism_species_1 = self.world._get_organism_at(4, 1)
        self.assertTrue(organism_species_1)
        self.assertEqual(organism_species_1.species, 2)
        self.assertTrue(self.world._get_organism_at(4, 3))
        # checking some of survived ones
        self.assertTrue(self.world._get_organism_at(0, 2))
        self.assertTrue(self.world._get_organism_at(3, 1))

    def test_iterate_no_evolution(self):
        self.world.organism_l = []
        self.world.populate_initial_organisms()
        self.world.iterate()

        self.assertEqual(self.world.organism_l, [])
        self.assertEqual(len(self.world.organism_l), 0)
        self.assertEqual(len(self.world._get_all_organisms()), 0)
